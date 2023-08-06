# -*- coding: utf-8 -*-

from seishub.core.exceptions import InvalidParameterError, NotFoundError, \
    InvalidObjectError
from seishub.core.util.xml import addXMLDeclaration, applyMacros
from seishub.core.xmldb.index import XmlIndex, TEXT_INDEX, INDEX_TYPES
from seishub.core.xmldb.interfaces import IResource
from seishub.core.xmldb.resource import Resource, newXMLDocument
from seishub.core.xmldb.xmldbms import XmlDbManager
from seishub.core.xmldb.xmlindexcatalog import XmlIndexCatalog
from seishub.core.xmldb.xpath import XPathQuery
import os


class XmlCatalog(object):
    """
    The catalog object.
    
    Use this class to manage all indexes and resources.
    """
    def __init__(self, env):
        self.env = env
        self.xmldb = XmlDbManager(env.db)
        self.index_catalog = XmlIndexCatalog(env.db, self.xmldb)
        self.index_catalog.env = env

    def addResource(self, package_id, resourcetype_id, xml_data, uid=None,
                    name=None):
        """
        Add a new resource to the database.
        
        @param package_id: package id
        @param resourcetype_id: resourcetype id
        @param xml_data: xml data
        @param uid: user id of creator
        @param name: optional resource name, defaults to unique integer id
        @return: Resource object
        """
        _, resourcetype = self.env.registry.objects_from_id(package_id,
                                                            resourcetype_id)
        res = Resource(resourcetype,
                       document=newXMLDocument(xml_data, uid=uid),
                       name=name)
        # get xml_doc to ensure the document is parsed
        res.document.xml_doc
        self.validateResource(res)
        self.xmldb.addResource(res)
        self.index_catalog.indexResource(res)
        return res

    def renameResource(self, resource, new_name):
        """
        Rename a given Resource object.
        """
        self.xmldb.renameResource(resource, new_name)

    def modifyResource(self, resource, xml_data, uid=None):
        """
        Modify the XML document of an already existing resource.
        
        In case of a version controlled resource a new revision is created.
        """
        new_resource = Resource(resourcetype=resource.resourcetype,
                                document=newXMLDocument(xml_data),
                                name=resource.name)
        self.validateResource(new_resource)
        self.xmldb.modifyResource(resource, new_resource, uid)
        # we only keep indexes for the newest revision
        self.index_catalog.flushResource(resource)
        self.index_catalog.indexResource(new_resource)

    def deleteResource(self, resource=None, resource_id=None):
        """
        Remove a resource from the database.
        """
        if resource_id:
            resource = self.xmldb.getResource(id=resource_id)
        # create backup entry into the global trash folder
        if self.env.config.getbool('seishub', 'use_trash_folder', False):
            data = resource.document.data
            # ensure we return a UTF-8 encoded string not an Unicode object 
            if isinstance(data, unicode):
                data = data.encode('utf-8')
            # set XML declaration inclusive UTF-8 encoding string 
            if not data.startswith('<xml'):
                data = addXMLDeclaration(data, 'utf-8')
            path = os.path.join(self.env.getInstancePath(), 'data', 'trash',
                                resource.package.package_id,
                                resource.resourcetype.resourcetype_id)
            if not os.path.exists(path):
                os.makedirs(path)
            file = os.path.join(path, resource.name)
            try:
                fp = open(file, 'wb')
                fp.write(data)
                fp.close()
            except:
                pass
        # remove indexed data:
        self.index_catalog.flushResource(resource)
        res = self.xmldb.deleteResource(resource)
        if not res:
            msg = "Error deleting a resource: No resource was found with " + \
                  "the given parameters."
            raise NotFoundError(msg)
        return res

    def deleteAllResources(self, package_id, resourcetype_id=None):
        """
        Remove all resources of specified package_id and resourcetype_id.
        """
        return self.xmldb.deleteAllResources(package_id, resourcetype_id)

    def getResource(self, package_id=None, resourcetype_id=None,
                    name=None, revision=None, document_id=None,
                    id=None):
        """
        Get a specific resource from the database.
        
        @param package_id: resourcetype id
        @param: resourcetype_id: package id
        @param name: Name of the resource
        @param revision: revision of related document (if no revision is given,
            newest revision is used, to retrieve all revisions of a document  
            use getRevisions()
        """
        return self.xmldb.getResource(package_id=package_id,
                                      resourcetype_id=resourcetype_id,
                                      name=name,
                                      revision=revision,
                                      document_id=document_id,
                                      id=id)

    def getRevisions(self, package_id, resourcetype_id, name):
        """
        Get all revisions of the specified resource.
        
        The Resource instance returned will contain a list of documents sorted 
        by revision (accessible as usual via Resource.document).
        Note: In case a resource does not provide multiple revisions, this is 
        the same as a call to XmlCatalog.getResource(...).
        
        @param package_id: package id
        @param resourcetype_id: resourcetype id
        @param name: name of the resource
        @return: Resource object
        """
        return self.xmldb.getRevisions(package_id, resourcetype_id, name)

    def getAllResources(self, package_id=None, resourcetype_id=None):
        """
        Get a list of resources for specified package and resourcetype.
        """
        return self.xmldb.getAllResources(package_id, resourcetype_id)
#    
#    def revertResource(self, package_id, resourcetype_id, name, revision):
#        """
#        Reverts the specified revision for the given resource.
#        
#        All revisions newer than the specified one will be removed.
#        """
#        return self.xmldb.revertResource(package_id, resourcetype_id, name, 
#                                         revision)

    def validateResource(self, resource):
        """
        Do a schema validation of a given resource.
        
        This validates against all schemas of the corresponding resourcetype.
        """
        pid = resource.package.package_id
        rid = resource.resourcetype.resourcetype_id
        schemas = self.env.registry.schemas.get(pid, rid)
        for schema in schemas:
            try:
                schema.validate(resource)
            except Exception, e:
                msg = "Resource-validation against schema '%s' failed. (%s)"
                raise InvalidObjectError(msg % (str(schema.getResource().name),
                                                str(e)))

    def registerIndex(self, package_id=None, resourcetype_id=None,
                      label=None, xpath=None, type="text",
                      options=None):
        """
        Register an index.
        
        @param type: "text" | "numeric" | "float" | "datetime" | "boolean" |
                     "date" | "integer" | "timestamp"
        """
        # check for label
        if not label:
            msg = "registerIndex: No index label defined!"
            raise InvalidParameterError(msg)
        if '/' in label:
            msg = "registerIndex: Label may not include an slash!"
            raise InvalidParameterError(msg)
        if len(label) > 30:
            msg = "registerIndex: Label may not exceed 30 chars!"
            raise InvalidParameterError(msg)
        # check for XPath expression
        if not xpath:
            msg = "registerIndex: Empty XPath expression!"
            raise InvalidParameterError(msg)
        # check if valid index type
        if type.lower() not in INDEX_TYPES:
            msg = "registerIndex: Invalid index type '%s'."
            raise InvalidParameterError(msg % type)
        # check for grouping indexes
        xpath = xpath.strip()
        group_path = None
        if '#' in xpath:
            try:
                group_path, temp = xpath.split('#')
            except ValueError, e:
                msg = "registerIndex: Invalid index expression. %s"
                raise InvalidParameterError(msg % str(e))
            xpath = '/'.join([group_path, temp])
        type = INDEX_TYPES.get(type.lower())
        _, resourcetype = self.env.registry.objects_from_id(package_id,
                                                            resourcetype_id)
        # generate index
        xmlindex = XmlIndex(resourcetype=resourcetype, label=label,
                            xpath=xpath, type=type, options=options,
                            group_path=group_path)
        xmlindex = self.index_catalog.registerIndex(xmlindex)
        return xmlindex

    def deleteIndex(self, xmlindex=None, _id=None):
        """
        Remove an index using either a XMLIndex object or a index id.
        """
        if _id:
            xmlindex = self.getIndexes(_id=_id)[0]
        self.index_catalog.deleteIndex(xmlindex)

    def deleteAllIndexes(self, package_id, resourcetype_id=None):
        """
        Removes all indexes related to a given package_id and resourcetype_id.
        """
        xmlindex_list = self.getIndexes(package_id=package_id,
                                        resourcetype_id=resourcetype_id)
        for xmlindex in xmlindex_list:
            self.deleteIndex(xmlindex)

    def getIndexes(self, package_id=None, resourcetype_id=None,
                   xpath=None, group_path=None, type=None,
                   options=None, _id=None, label=None):
        """
        Return a list of all applicable XMLIndex objects.
        """
        # check for grouping indexes
        if xpath and '#' in xpath:
            group_path, temp = xpath.split('#', 1)
            xpath = '/'.join([group_path, temp])
        if type:
            type = INDEX_TYPES.get(type.lower(), TEXT_INDEX)
        return self.index_catalog.getIndexes(package_id=package_id,
                                             resourcetype_id=resourcetype_id,
                                             xpath=xpath,
                                             group_path=group_path,
                                             type=type,
                                             options=options,
                                             _id=_id,
                                             label=label)

    def getIndexData(self, resource):
        """
        Return indexed data for a given Resource as dictionary.
        
        @param resource: resource
        @type resource: L{seishub.xmldb.interfaces.IResource}
        """
        if not IResource.providedBy(resource):
            msg = "getIndexData: Resource expected. Got a %s."
            raise TypeError(msg % type(resource))
        # sanity check: document should have an id, else no data can be found
        assert resource.document._id
        elements = self.index_catalog.dumpIndexByResource(resource)
        values = {}
        for element in elements:
            values.setdefault(element.index.label, {})
            if element.group_pos not in values[element.index.label]:
                values[element.index.label][element.group_pos] = list()
            values[element.index.label][element.group_pos].append(element.key)
        return values

    def query(self, query, full=False):
        """
        Query the catalog via restricted XPath queries.
        
        The values returned depend on the type of query:
        
        Is the location path of a query on resource level, i.e. on rootnode or 
        above (e.g. '/package/resourcetype/*'), ALL indexes known for that 
        resource are requested and returned as a dict.
        
        Does the location path address a node other than the rootnode (e.g.
        '/package/resourcetype/rootnode/node1/node2'), indexed data for that
        node ONLY is returned. 
        Note: The index '/package/resourcetype/rootnode/node1/node2' has to 
        exist, of course. 
        
        The result set is a dict of the form {document_ids : {xpath:value}, 
        ...}. 
        There is an additional key 'ordered' containing an ORDERED list of
        document ids, which is of interest in case there is an order by clause,
        as the dict itself does not preserve order.
        
        For further detail on the restricted XPath query syntax, see 
        L{seishub.xmldb.xpath}
        
        @param query: Restricted XPath query to be executed.
        @type query: basestring
        @param full: If True, picks the resource objects for the results
        @return: Either a list of Resource objects, or a dict
        """
        query = applyMacros(query)
        q = XPathQuery(query)
        results = self.index_catalog.query(q)
        if not full:
            return results
        return [self.xmldb.getResource(document_id=id)
                for id in results['ordered']]

    def updateAllIndexViews(self):
        """
        Updates all IndexViews.
        """
        self.env.log.debug("Updating IndexViews ...")
        xmlindex_list = self.getIndexes()
        rts = {}
        for xmlindex in xmlindex_list:
            if xmlindex.resourcetype._id not in rts:
                rts[xmlindex.resourcetype._id] = xmlindex.resourcetype
        for rt in rts.values():
            self.index_catalog.updateIndexView(rt)
        self.env.log.info("IndexViews have been updated.")

    def getAllResourceNames(self, package_id, resourcetype_id, limit=100,
                            ordered=False):
        """
        Return a list of all resource names of given package and resource type.
        """
        _, resourcetype = self.env.registry.objects_from_id(package_id,
                                                            resourcetype_id)
        return self.xmldb.getAllResourceNames(resourcetype, limit, ordered)

    def reindexIndex(self, xmlindex=None, _id=None):
        """
        Reindex all resources by a given XMLIndex object.
        """
        if _id:
            xmlindex = self.getIndexes(_id=_id)[0]
        return self.index_catalog.reindexIndexes([xmlindex])

    def reindexResourceType(self, package_id, resourcetype_id):
        """
        Reindex a whole resource type by given package_id and resourcetype_id.
        """
        xmlindex_list = self.getIndexes(package_id=package_id,
                                        resourcetype_id=resourcetype_id)
        if not xmlindex_list:
            return
        return self.index_catalog.reindexIndexes(xmlindex_list)

    def reindexResource(self, resource):
        """
        Reindex a single, given Resource object.
        """
        self.index_catalog.flushResource(resource)
        self.index_catalog.indexResource(resource)
