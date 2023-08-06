import ckanclient
import urllib
from pprint import pformat

from ordf.graph import Graph
from ordf.namespace import DC, DCAT, FOAF, LICENSES, OWL, RDF, RDFS, REV, SCOVO, UUID, VOID, XSD
from ordf.term import URIRef as _URIRef, Literal as _Literal, BNode
from ordf.vocab.opmv import Agent, Process

log = __import__("logging").getLogger("ckanrdf.package")

#
# CKAN gives us data HTML escaped. We don't want that
# when storing with RDFLib. So this function and the
# two wrappers for Literal and URIRef de-escape the
# characters
#
from htmlentitydefs import name2codepoint
import re
_htmle_re = re.compile('&(%s);' % '|'.join(name2codepoint))
def htmlentitydecode(s):
    try:
        return _htmle_re.sub(lambda m: unichr(name2codepoint[m.group(1)]), s)
    except UnicodeError:
        return s
def Literal(x, *av, **kw):
    if isinstance(x, basestring):
        return _Literal(htmlentitydecode(x.strip()), *av, **kw)
    return _Literal(x, *av, **kw)

def URIRef(x, *av, **kw):
    clean = htmlentitydecode(x.strip())
    p,q = urllib.splitquery(clean)
    if q:
        uri = p + "?" + q.replace(":", "%3a"
                            ).replace("/", "%2f"
                            )
    else:
        uri = p
    return _URIRef(uri, *av, **kw)

class Tag(object):
    def __init__(self, config):
        self.config = config
    def tag_base(self):
        return self.config.get("ckan_tag_base",
                               self.ckan_base() + "tag/")
    def tag_uri(self, tagname):
        return URIRef(self.tag_base() + tagname)

class Package(object):
    def __init__(self, config):
        self.config = config
        self.tags = Tag(config)

    def ckan_base(self):
        return self.config.get("ckan_base", "http://ckan.net/")

    def pkg_base(self):
        return self.config.get("ckan_pkg_base",
                               self.ckan_base() + "package/")
    def pkg_uri(self, data):
        if "ckan_url" in data and data["ckan_url"]:
            uri = data["ckan_url"]
            del data["ckan_url"]
            return URIRef(uri)
        return URIRef(self.pkg_base() + data["name"])

    def rdf_base(self):
        return self.config.get("rdf_base", "http://semantic.ckan.net/")
    def rdf_cat_base(self):
        return self.config.get("rdf_cat_base", self.rdf_base() + "catalogue")
    def rdf_pkg_base(self):
        return self.config.get("rdf_pkg_base", self.rdf_base() + "package/")
    def rdf_pkg_uri(self, data):
        return URIRef(self.rdf_pkg_base() + data["name"][0] + "/" + data["name"][1] + "/" + data["name"])
    def sparql_endpoint(self):
        return self.config.get("sparql_endpoint", "http://semantic.ckan.net/sparql")

    def build_catalogue(self, packages, store="IOMemory"):
        rdf_uri = URIRef(self.rdf_cat_base())
        catalogue = Graph(store, identifier=rdf_uri)
        catalogue.remove((None, None, None))
        catalogue.add((rdf_uri, RDF["type"], DCAT["Catalog"]))
        catalogue.add((rdf_uri, RDF["type"], VOID["Dataset"]))
        catalogue.add((rdf_uri, DC.publisher,
                       URIRef(self.config.get("rdf_publisher", "http://ckan.net/"))))
        catalogue.add((rdf_uri, VOID["sparqlEndpoint"], URIRef(self.sparql_endpoint())))

        for pkg in packages:
            catalogue.add((rdf_uri, DCAT.record, self.rdf_pkg_uri(pkg)))

        return catalogue

    def describe(self, data, store="IOMemory"):
        log.info("Describing %(name)s" % data)
        uri = self.pkg_uri(data)
        rdf_uri = self.rdf_pkg_uri(data)

        rec = Graph(store, identifier=rdf_uri)
        rec.remove((None, None, None))
        rec.add((rdf_uri, RDF["type"], DCAT["CatalogRecord"]))
        rec.add((rdf_uri, DC["publisher"],
                    URIRef(self.config.get("rdf_publisher", "http://ckan.net/"))))
        rec.add((rdf_uri, DCAT["dataset"], uri))

        rec.add((uri, RDF["type"], DCAT["Dataset"]))
        rec.add((uri, OWL["sameAs"], UUID[data["id"]]))
        rec.add((uri, DC["identifier"], Literal(data["name"])))
        del data["id"]
        del data["name"]

        if data["url"] is not None:
            rec.add((uri, FOAF["homepage"], URIRef(data["url"])))
        del data["url"]

        if data["title"] is not None:
            rec.add((uri, RDFS["label"], Literal(data["title"])))
            rec.add((uri, DC["title"], Literal(data["title"])))
        del data["title"]

        if data["notes"] is not None:
            rec.add((uri, DC["description"], Literal(data["notes"])))
        del data["notes"]

        if data["license_id"] is not None:
            rec.add((uri, DC["rights"], LICENSES[data["license_id"]]))
        del data["license"]
        del data["license_id"]

        author = BNode()
        if data["author"] or data["author_email"]:
            rec.add((uri,DC.creator, author))
        if data["author"]:
            rec.add((author,FOAF.name, Literal(data["author"])))
        if data["author_email"]:
            rec.add((author,FOAF.mbox, URIRef("mailto:" + data["author_email"])))
        del data["author"]
        del data["author_email"]

        maintainer = BNode()
        if data["maintainer"] or data["maintainer_email"]:
            rec.add((uri,DC.contributor, maintainer))
        if data["maintainer"]:
            rec.add((maintainer,FOAF.name, Literal(data["maintainer"])))
        if data["maintainer_email"]:
            rec.add((maintainer,FOAF.mbox, URIRef("mailto:" + data["maintainer_email"])))
        del data["maintainer"]
        del data["maintainer_email"]

        for tag in data["tags"]:
            rec.add((uri, DCAT["keyword"], Literal(tag)))
        del data["tags"]

        if data["ratings_average"] is not None:
            rec.add((uri,REV.rating,
                     Literal(data["ratings_average"], datatype=XSD.float)))
        # can't useREV.totalVotes since that implies being a Review
        # ask Mr. Ayers
        #if data["ratings_count"] is not None:
        #    g.add((uri,REV.totalVotes,
        #           Literal(data["ratings_count"], datatype=XSD.integer)))
        del data["ratings_average"]
        del data["ratings_count"]

        for rdata in data["resources"]:
            self._process_resources(rec, uri, rdata)
        del data["download_url"]
        del data["resources"]

        for k,v in data["extras"].items():
            self._process_extra(rec, uri, k, v)
        del data["extras"]

        for rdata in data["relationships"]:
            self._process_relationship(rec, uri, rdata)
        del data["relationships"]

        ## TODO handle groups and version
        del data["groups"]
        del data["version"]

        ## TODO something with these?
        del data["revision_id"]
        del data["state"]

        if data:
            log.info("Unhandled information in %s:\n%s" % (uri, pformat(data)))
        return rec

    def _process_resources(self, rec, uri, rdata):
        if rdata["format"] == "api/sparql":
            ## RDF datasets with SPARQL endpoints are marked so by LOD
            rec.add((uri, RDF["type"], VOID["Dataset"]))
            rec.add((uri, VOID["sparqlEndpoint"], URIRef(rdata["url"])))
        elif rdata["format"] == "meta/rdf-schema":
            rec.add((uri, RDF["type"], VOID["Dataset"]))
            rec.add((uri, VOID["vocabulary"], URIRef("http://www.w3.org/2000/01/rdf-schema#")))
        elif rdata["format"] == "meta/void":
            rec.add((uri, RDF["type"], VOID["Dataset"]))
            rec.add((uri, VOID["vocabulary"], VOID[""]))
        elif rdata["format"] in ("application/x-ntriples", "application/x-nquads", "application/rdf+xml", "text/n3", "text/turtle"):
            rec.add((uri, RDF["type"], VOID["Dataset"]))
            dump = URIRef(rdata["url"])
            rec.add((uri, VOID["dataDump"], dump))
            format = self.get_format(rdata["format"])
            rec.add((dump, DC["format"], format.identifier))
            rec += format
        elif rdata["format"] in ("example/rdf+xml", "example/turtle", "example/rdfa"):
            subset = BNode()
            rec.add((uri, VOID["subset"], subset))
            rec.add((subset, RDF["type"], VOID["Dataset"]))
            resource = BNode()
            rec.add((subset, DCAT["distribution"], resource))
            rec.add((resource, RDF["type"], DCAT["Distribution"]))
            rec.add((resource, DCAT["accessURL"], URIRef(rdata["url"])))
            format = self.get_format(rdata["format"])
            rec.add((resource, DC["format"], format.identifier))
            rec += format
            if rdata["description"]:
                rec.add((resource, RDFS["label"], Literal(rdata["description"])))
        else:
            resource = BNode()
            rec.add((uri, DCAT["distribution"], resource))
            rec.add((resource, RDF["type"], DCAT["Distribution"]))
            rec.add((resource, DCAT["accessURL"], URIRef(rdata["url"])))
            if rdata["format"]:
                format = self.get_format(rdata["format"])
                rec.add((resource, DC["format"], format.identifier))
                rec += format
            if rdata["description"]:
                rec.add((resource, RDFS["label"], Literal(rdata["description"])))

    def get_format(self, format):
        g = Graph()
        if format == "example/rdf+xml":
            g.add((g.identifier, RDF["type"], DC["IMT"]))
            g.add((g.identifier, RDF["value"], Literal("application/rdf+xml")))
            g.add((g.identifier, RDFS["label"], Literal("RDF/XML")))
        elif format == "example/turtle":
            g.add((g.identifier, RDF["type"], DC["IMT"]))
            g.add((g.identifier, RDF["value"], Literal("text/turtle")))
            g.add((g.identifier, RDFS["label"], Literal("RDF/Turtle")))
        elif format == "example/ntriples":
            g.add((g.identifier, RDF["type"], DC["IMT"]))
            g.add((g.identifier, RDF["value"], Literal("application/x-ntriples")))
            g.add((g.identifier, RDFS["label"], Literal("RDF/N-Triples")))
        elif format == "example/rdfa":
            g.add((g.identifier, RDF["type"], DC["IMT"]))
            g.add((g.identifier, RDF["value"], Literal("application/xhtml+xml")))
            g.add((g.identifier, RDFS["label"], Literal("RDFa")))
        elif format in ("application/x-ntriples", "application/x-nquads", "application/rdf+xml", "text/n3", "text/turtle"):
            g.add((g.identifier, RDF["type"], DC["IMT"]))
            g.add((g.identifier, RDF["value"], Literal(format)))
            g.add((g.identifier, RDFS["label"], Literal(format)))
        elif format in ("meta/sitemap",):
            g.add((g.identifier, RDFS["label"], Literal(format)))
        else:
            log.warning("Unknown format: %s" % format)
            g.add((g.identifier, RDFS["label"], Literal(format)))
        return g

    def _process_extra(self, rec, uri, key, value):
        if key.startswith("links:"):
            self._process_linkset(rec, uri, key, value)
        elif key == "triples":
            rec.add((uri, RDF["type"], VOID["Dataset"]))
            count = BNode()
            rec.add((uri, VOID["statItem"], count))
            rec.add((count, SCOVO["dimension"], VOID["numberOfTriples"]))
            rec.add((count, RDF["value"], Literal(int(value))))
        else:
            log.warning("Unknown extra in %s: %s = %s" % (uri.rsplit("/", 1)[-1], key, value))

    def _process_relationship(self, rec, uri, rdata):
        if rdata["type"] == "linked_from":
            pass
        else:
            log.warning("Unknown relationship in %s: %s" % (uri.rsplit("/", 1)[-1], rdata))

    def _process_linkset(self, rec, uri, key, value):
        _unused, target = key.split(":")
        target = self.pkg_uri({ "name" : target })
        linkset = BNode()
        rec.add((uri, VOID["subset"], linkset))
        rec.add((linkset, RDF["type"], VOID["Linkset"]))
        rec.add((linkset, VOID["subjectTarget"], uri))
        rec.add((linkset, VOID["objectTarget"], target))
        count = BNode()
        rec.add((linkset, VOID["statItem"], count))
        rec.add((count, SCOVO["dimension"], VOID["numberOfTriples"]))
        rec.add((count, RDF["value"], Literal(int(value))))
