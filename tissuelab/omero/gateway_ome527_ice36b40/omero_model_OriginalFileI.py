"""
   /*
   **   Generated by blitz/resources/templates/combined.vm
   **
   **   Copyright 2007, 2008 Glencoe Software, Inc. All rights reserved.
   **   Use is subject to license terms supplied in LICENSE.txt
   **
   */
"""
import Ice
import IceImport
import omero
IceImport.load("omero_model_DetailsI")
IceImport.load("omero_model_OriginalFile_ice")
from omero.rtypes import rlong
from collections import namedtuple
_omero = Ice.openModule("omero")
_omero_model = Ice.openModule("omero.model")
__name__ = "omero.model"
class OriginalFileI(_omero_model.OriginalFile):

      # Property Metadata
      _field_info_data = namedtuple("FieldData", ["wrapper", "nullable"])
      _field_info_type = namedtuple("FieldInfo", [
          "pixelsFileMaps",
          "path",
          "size",
          "atime",
          "mtime",
          "ctime",
          "hasher",
          "hash",
          "mimetype",
          "filesetEntries",
          "annotationLinks",
          "name",
          "details",
      ])
      _field_info = _field_info_type(
          pixelsFileMaps=_field_info_data(wrapper=omero.proxy_to_instance, nullable=True),
          path=_field_info_data(wrapper=omero.rtypes.rstring, nullable=False),
          size=_field_info_data(wrapper=omero.rtypes.rlong, nullable=True),
          atime=_field_info_data(wrapper=omero.rtypes.rtime, nullable=True),
          mtime=_field_info_data(wrapper=omero.rtypes.rtime, nullable=True),
          ctime=_field_info_data(wrapper=omero.rtypes.rtime, nullable=True),
          hasher=_field_info_data(wrapper=omero.proxy_to_instance, nullable=True),
          hash=_field_info_data(wrapper=omero.rtypes.rstring, nullable=True),
          mimetype=_field_info_data(wrapper=omero.rtypes.rstring, nullable=True),
          filesetEntries=_field_info_data(wrapper=omero.proxy_to_instance, nullable=True),
          annotationLinks=_field_info_data(wrapper=omero.proxy_to_instance, nullable=True),
          name=_field_info_data(wrapper=omero.rtypes.rstring, nullable=False),
          details=_field_info_data(wrapper=omero.proxy_to_instance, nullable=True),
      )  # end _field_info
      PIXELSFILEMAPS =  "ome.model.core.OriginalFile_pixelsFileMaps"
      PATH =  "ome.model.core.OriginalFile_path"
      SIZE =  "ome.model.core.OriginalFile_size"
      ATIME =  "ome.model.core.OriginalFile_atime"
      MTIME =  "ome.model.core.OriginalFile_mtime"
      CTIME =  "ome.model.core.OriginalFile_ctime"
      HASHER =  "ome.model.core.OriginalFile_hasher"
      HASH =  "ome.model.core.OriginalFile_hash"
      MIMETYPE =  "ome.model.core.OriginalFile_mimetype"
      FILESETENTRIES =  "ome.model.core.OriginalFile_filesetEntries"
      ANNOTATIONLINKS =  "ome.model.core.OriginalFile_annotationLinks"
      NAME =  "ome.model.core.OriginalFile_name"
      DETAILS =  "ome.model.core.OriginalFile_details"
      def errorIfUnloaded(self):
          if not self._loaded:
              raise _omero.UnloadedEntityException("Object unloaded:"+str(self))

      def throwNullCollectionException(self,propertyName):
          raise _omero.UnloadedEntityException(""+
          "Error updating collection:" + propertyName +"\n"+
          "Collection is currently null. This can be seen\n" +
          "by testing \""+ propertyName +"Loaded\". This implies\n"+
          "that this collection was unloaded. Please refresh this object\n"+
          "in order to update this collection.\n")

      def _toggleCollectionsLoaded(self, load):
          if load:
              self._pixelsFileMapsSeq = []
              self._pixelsFileMapsLoaded = True;
          else:
              self._pixelsFileMapsSeq = []
              self._pixelsFileMapsLoaded = False;

          if load:
              self._filesetEntriesSeq = []
              self._filesetEntriesLoaded = True;
          else:
              self._filesetEntriesSeq = []
              self._filesetEntriesLoaded = False;

          if load:
              self._annotationLinksSeq = []
              self._annotationLinksLoaded = True;
          else:
              self._annotationLinksSeq = []
              self._annotationLinksLoaded = False;

          pass

      def __init__(self, id=None, loaded=None):
          super(OriginalFileI, self).__init__()
          if id is not None and isinstance(id, (str, unicode)) and ":" in id:
              parts = id.split(":")
              if len(parts) != 2:
                  raise Exception("Invalid proxy string: %s", id)
              if parts[0] != self.__class__.__name__ and \
                 parts[0]+"I" != self.__class__.__name__:
                  raise Exception("Proxy class mismatch: %s<>%s" %
                  (self.__class__.__name__, parts[0]))
              self._id = rlong(parts[1])
              if loaded is None:
                  # If no loadedness was requested with
                  # a proxy string, then assume False.
                  loaded = False
          else:
              # Relying on omero.rtypes.rlong's error-handling
              self._id = rlong(id)
              if loaded is None:
                  loaded = True  # Assume true as previously
          self._loaded = loaded
          if self._loaded:
             self._details = _omero_model.DetailsI()
             self._toggleCollectionsLoaded(True)

      def unload(self, current = None):
          self._loaded = False
          self.unloadPixelsFileMaps( )
          self.unloadPath( )
          self.unloadSize( )
          self.unloadAtime( )
          self.unloadMtime( )
          self.unloadCtime( )
          self.unloadHasher( )
          self.unloadHash( )
          self.unloadMimetype( )
          self.unloadFilesetEntries( )
          self.unloadAnnotationLinks( )
          self.unloadName( )
          self.unloadDetails( )

      def isLoaded(self, current = None):
          return self._loaded
      def unloadCollections(self, current = None):
          self._toggleCollectionsLoaded( False )
      def isGlobal(self, current = None):
          return  False ;
      def isMutable(self, current = None):
          return  True ;
      def isAnnotated(self, current = None):
          return  True ;
      def isLink(self, current = None):
          return  False ;
      def shallowCopy(self, current = None):
            if not self._loaded: return self.proxy()
            copy = OriginalFileI()
            copy._id = self._id;
            copy._version = self._version;
            copy._details = None  # Unloading for the moment.
            raise omero.ClientError("NYI")
      def proxy(self, current = None):
          if self._id is None: raise omero.ClientError("Proxies require an id")
          return OriginalFileI( self._id.getValue(), False )

      def getDetails(self, current = None):
          self.errorIfUnloaded()
          return self._details

      def unloadDetails(self, current = None):
          self._details = None

      def getId(self, current = None):
          return self._id

      def setId(self, _id, current = None):
          self._id = _id

      def checkUnloadedProperty(self, value, loadedField):
          if value == None:
              self.__dict__[loadedField] = False
          else:
              self.__dict__[loadedField] = True

      def getVersion(self, current = None):
          self.errorIfUnloaded()
          return self._version

      def setVersion(self, version, current = None):
          self.errorIfUnloaded()
          self._version = version

      def unloadPixelsFileMaps(self, current = None):
          self._pixelsFileMapsLoaded = False
          self._pixelsFileMapsSeq = None;

      def _getPixelsFileMaps(self, current = None):
          self.errorIfUnloaded()
          return self._pixelsFileMapsSeq

      def _setPixelsFileMaps(self, _pixelsFileMaps, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.pixelsFileMapsSeq.wrapper is not None:
              if _pixelsFileMaps is not None:
                  _pixelsFileMaps = self._field_info.pixelsFileMapsSeq.wrapper(_pixelsFileMaps)
          self._pixelsFileMapsSeq = _pixelsFileMaps
          self.checkUnloadedProperty(_pixelsFileMaps,'pixelsFileMapsLoaded')

      def isPixelsFileMapsLoaded(self):
          return self._pixelsFileMapsLoaded

      def sizeOfPixelsFileMaps(self, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: return -1
          return len(self._pixelsFileMapsSeq)

      def copyPixelsFileMaps(self, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          return list(self._pixelsFileMapsSeq)

      def iteratePixelsFileMaps(self):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          return iter(self._pixelsFileMapsSeq)

      def addPixelsOriginalFileMap(self, target, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          self._pixelsFileMapsSeq.append( target );
          target.setParent( self )

      def addAllPixelsOriginalFileMapSet(self, targets, current = None):
          self.errorIfUnloaded()
          if  not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          self._pixelsFileMapsSeq.extend( targets )
          for target in targets:
              target.setParent( self )

      def removePixelsOriginalFileMap(self, target, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          self._pixelsFileMapsSeq.remove( target )
          target.setParent( None )

      def removeAllPixelsOriginalFileMapSet(self, targets, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          for elt in targets:
              elt.setParent( None )
              self._pixelsFileMapsSeq.remove( elt )

      def clearPixelsFileMaps(self, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          for elt in self._pixelsFileMapsSeq:
              elt.setParent( None )
          self._pixelsFileMapsSeq = list()

      def reloadPixelsFileMaps(self, toCopy, current = None):
          self.errorIfUnloaded()
          if self._pixelsFileMapsLoaded:
              raise omero.ClientError("Cannot reload active collection: pixelsFileMapsSeq")
          if not toCopy:
              raise omero.ClientError("Argument cannot be null")
          if toCopy.getId().getValue() != self.getId().getValue():
             raise omero.ClientError("Argument must have the same id as this instance")
          if toCopy.getDetails().getUpdateEvent().getId().getValue() < self.getDetails().getUpdateEvent().getId().getValue():
             raise omero.ClientError("Argument may not be older than this instance")
          copy = toCopy.copyPixelsFileMaps() # May also throw
          for elt in copy:
              elt.setParent( self )
          self._pixelsFileMapsSeq = copy
          toCopy.unloadPixelsFileMaps()
          self._pixelsFileMapsLoaded = True

      def getPixelsFileMapsCountPerOwner(self, current = None):
          return self._pixelsFileMapsCountPerOwner

      def linkPixels(self, addition, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          link = _omero_model.PixelsOriginalFileMapI()
          link.link( self, addition );
          self.addPixelsOriginalFileMapToBoth( link, True )
          return link

      def addPixelsOriginalFileMapToBoth(self, link, bothSides):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          self._pixelsFileMapsSeq.append( link )
          if bothSides and link.getChild().isLoaded():
              link.getChild().addPixelsOriginalFileMapToBoth( link, False )

      def findPixelsOriginalFileMap(self, removal, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          result = list()
          for link in self._pixelsFileMapsSeq:
              if link.getChild() == removal: result.append(link)
          return result

      def unlinkPixels(self, removal, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          toRemove = self.findPixelsOriginalFileMap(removal)
          for next in toRemove:
              self.removePixelsOriginalFileMapFromBoth( next, True )

      def removePixelsOriginalFileMapFromBoth(self, link, bothSides, current = None):
          self.errorIfUnloaded()
          if not self._pixelsFileMapsLoaded: self.throwNullCollectionException("pixelsFileMapsSeq")
          self._pixelsFileMapsSeq.remove( link )
          if bothSides and link.getChild().isLoaded():
              link.getChild().removePixelsOriginalFileMapFromBoth(link, False)

      def linkedPixelsList(self, current = None):
          self.errorIfUnloaded()
          if not self.pixelsFileMapsLoaded: self.throwNullCollectionException("PixelsFileMaps")
          linked = []
          for link in self._pixelsFileMapsSeq:
              linked.append( link.getChild() )
          return linked

      def unloadPath(self, ):
          self._pathLoaded = False
          self._path = None;

      def getPath(self, current = None):
          self.errorIfUnloaded()
          return self._path

      def setPath(self, _path, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.path.wrapper is not None:
              if _path is not None:
                  _path = self._field_info.path.wrapper(_path)
          self._path = _path
          pass

      def unloadSize(self, ):
          self._sizeLoaded = False
          self._size = None;

      def getSize(self, current = None):
          self.errorIfUnloaded()
          return self._size

      def setSize(self, _size, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.size.wrapper is not None:
              if _size is not None:
                  _size = self._field_info.size.wrapper(_size)
          self._size = _size
          pass

      def unloadAtime(self, ):
          self._atimeLoaded = False
          self._atime = None;

      def getAtime(self, current = None):
          self.errorIfUnloaded()
          return self._atime

      def setAtime(self, _atime, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.atime.wrapper is not None:
              if _atime is not None:
                  _atime = self._field_info.atime.wrapper(_atime)
          self._atime = _atime
          pass

      def unloadMtime(self, ):
          self._mtimeLoaded = False
          self._mtime = None;

      def getMtime(self, current = None):
          self.errorIfUnloaded()
          return self._mtime

      def setMtime(self, _mtime, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.mtime.wrapper is not None:
              if _mtime is not None:
                  _mtime = self._field_info.mtime.wrapper(_mtime)
          self._mtime = _mtime
          pass

      def unloadCtime(self, ):
          self._ctimeLoaded = False
          self._ctime = None;

      def getCtime(self, current = None):
          self.errorIfUnloaded()
          return self._ctime

      def setCtime(self, _ctime, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.ctime.wrapper is not None:
              if _ctime is not None:
                  _ctime = self._field_info.ctime.wrapper(_ctime)
          self._ctime = _ctime
          pass

      def unloadHasher(self, ):
          self._hasherLoaded = False
          self._hasher = None;

      def getHasher(self, current = None):
          self.errorIfUnloaded()
          return self._hasher

      def setHasher(self, _hasher, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.hasher.wrapper is not None:
              if _hasher is not None:
                  _hasher = self._field_info.hasher.wrapper(_hasher)
          self._hasher = _hasher
          pass

      def unloadHash(self, ):
          self._hashLoaded = False
          self._hash = None;

      def getHash(self, current = None):
          self.errorIfUnloaded()
          return self._hash

      def setHash(self, _hash, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.hash.wrapper is not None:
              if _hash is not None:
                  _hash = self._field_info.hash.wrapper(_hash)
          self._hash = _hash
          pass

      def unloadMimetype(self, ):
          self._mimetypeLoaded = False
          self._mimetype = None;

      def getMimetype(self, current = None):
          self.errorIfUnloaded()
          return self._mimetype

      def setMimetype(self, _mimetype, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.mimetype.wrapper is not None:
              if _mimetype is not None:
                  _mimetype = self._field_info.mimetype.wrapper(_mimetype)
          self._mimetype = _mimetype
          pass

      def unloadFilesetEntries(self, current = None):
          self._filesetEntriesLoaded = False
          self._filesetEntriesSeq = None;

      def _getFilesetEntries(self, current = None):
          self.errorIfUnloaded()
          return self._filesetEntriesSeq

      def _setFilesetEntries(self, _filesetEntries, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.filesetEntriesSeq.wrapper is not None:
              if _filesetEntries is not None:
                  _filesetEntries = self._field_info.filesetEntriesSeq.wrapper(_filesetEntries)
          self._filesetEntriesSeq = _filesetEntries
          self.checkUnloadedProperty(_filesetEntries,'filesetEntriesLoaded')

      def isFilesetEntriesLoaded(self):
          return self._filesetEntriesLoaded

      def sizeOfFilesetEntries(self, current = None):
          self.errorIfUnloaded()
          if not self._filesetEntriesLoaded: return -1
          return len(self._filesetEntriesSeq)

      def copyFilesetEntries(self, current = None):
          self.errorIfUnloaded()
          if not self._filesetEntriesLoaded: self.throwNullCollectionException("filesetEntriesSeq")
          return list(self._filesetEntriesSeq)

      def iterateFilesetEntries(self):
          self.errorIfUnloaded()
          if not self._filesetEntriesLoaded: self.throwNullCollectionException("filesetEntriesSeq")
          return iter(self._filesetEntriesSeq)

      def addFilesetEntry(self, target, current = None):
          self.errorIfUnloaded()
          if not self._filesetEntriesLoaded: self.throwNullCollectionException("filesetEntriesSeq")
          self._filesetEntriesSeq.append( target );
          target.setOriginalFile( self )

      def addAllFilesetEntrySet(self, targets, current = None):
          self.errorIfUnloaded()
          if  not self._filesetEntriesLoaded: self.throwNullCollectionException("filesetEntriesSeq")
          self._filesetEntriesSeq.extend( targets )
          for target in targets:
              target.setOriginalFile( self )

      def removeFilesetEntry(self, target, current = None):
          self.errorIfUnloaded()
          if not self._filesetEntriesLoaded: self.throwNullCollectionException("filesetEntriesSeq")
          self._filesetEntriesSeq.remove( target )
          target.setOriginalFile( None )

      def removeAllFilesetEntrySet(self, targets, current = None):
          self.errorIfUnloaded()
          if not self._filesetEntriesLoaded: self.throwNullCollectionException("filesetEntriesSeq")
          for elt in targets:
              elt.setOriginalFile( None )
              self._filesetEntriesSeq.remove( elt )

      def clearFilesetEntries(self, current = None):
          self.errorIfUnloaded()
          if not self._filesetEntriesLoaded: self.throwNullCollectionException("filesetEntriesSeq")
          for elt in self._filesetEntriesSeq:
              elt.setOriginalFile( None )
          self._filesetEntriesSeq = list()

      def reloadFilesetEntries(self, toCopy, current = None):
          self.errorIfUnloaded()
          if self._filesetEntriesLoaded:
              raise omero.ClientError("Cannot reload active collection: filesetEntriesSeq")
          if not toCopy:
              raise omero.ClientError("Argument cannot be null")
          if toCopy.getId().getValue() != self.getId().getValue():
             raise omero.ClientError("Argument must have the same id as this instance")
          if toCopy.getDetails().getUpdateEvent().getId().getValue() < self.getDetails().getUpdateEvent().getId().getValue():
             raise omero.ClientError("Argument may not be older than this instance")
          copy = toCopy.copyFilesetEntries() # May also throw
          for elt in copy:
              elt.setOriginalFile( self )
          self._filesetEntriesSeq = copy
          toCopy.unloadFilesetEntries()
          self._filesetEntriesLoaded = True

      def unloadAnnotationLinks(self, current = None):
          self._annotationLinksLoaded = False
          self._annotationLinksSeq = None;

      def _getAnnotationLinks(self, current = None):
          self.errorIfUnloaded()
          return self._annotationLinksSeq

      def _setAnnotationLinks(self, _annotationLinks, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.annotationLinksSeq.wrapper is not None:
              if _annotationLinks is not None:
                  _annotationLinks = self._field_info.annotationLinksSeq.wrapper(_annotationLinks)
          self._annotationLinksSeq = _annotationLinks
          self.checkUnloadedProperty(_annotationLinks,'annotationLinksLoaded')

      def isAnnotationLinksLoaded(self):
          return self._annotationLinksLoaded

      def sizeOfAnnotationLinks(self, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: return -1
          return len(self._annotationLinksSeq)

      def copyAnnotationLinks(self, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          return list(self._annotationLinksSeq)

      def iterateAnnotationLinks(self):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          return iter(self._annotationLinksSeq)

      def addOriginalFileAnnotationLink(self, target, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          self._annotationLinksSeq.append( target );
          target.setParent( self )

      def addAllOriginalFileAnnotationLinkSet(self, targets, current = None):
          self.errorIfUnloaded()
          if  not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          self._annotationLinksSeq.extend( targets )
          for target in targets:
              target.setParent( self )

      def removeOriginalFileAnnotationLink(self, target, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          self._annotationLinksSeq.remove( target )
          target.setParent( None )

      def removeAllOriginalFileAnnotationLinkSet(self, targets, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          for elt in targets:
              elt.setParent( None )
              self._annotationLinksSeq.remove( elt )

      def clearAnnotationLinks(self, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          for elt in self._annotationLinksSeq:
              elt.setParent( None )
          self._annotationLinksSeq = list()

      def reloadAnnotationLinks(self, toCopy, current = None):
          self.errorIfUnloaded()
          if self._annotationLinksLoaded:
              raise omero.ClientError("Cannot reload active collection: annotationLinksSeq")
          if not toCopy:
              raise omero.ClientError("Argument cannot be null")
          if toCopy.getId().getValue() != self.getId().getValue():
             raise omero.ClientError("Argument must have the same id as this instance")
          if toCopy.getDetails().getUpdateEvent().getId().getValue() < self.getDetails().getUpdateEvent().getId().getValue():
             raise omero.ClientError("Argument may not be older than this instance")
          copy = toCopy.copyAnnotationLinks() # May also throw
          for elt in copy:
              elt.setParent( self )
          self._annotationLinksSeq = copy
          toCopy.unloadAnnotationLinks()
          self._annotationLinksLoaded = True

      def getAnnotationLinksCountPerOwner(self, current = None):
          return self._annotationLinksCountPerOwner

      def linkAnnotation(self, addition, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          link = _omero_model.OriginalFileAnnotationLinkI()
          link.link( self, addition );
          self.addOriginalFileAnnotationLinkToBoth( link, True )
          return link

      def addOriginalFileAnnotationLinkToBoth(self, link, bothSides):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          self._annotationLinksSeq.append( link )

      def findOriginalFileAnnotationLink(self, removal, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          result = list()
          for link in self._annotationLinksSeq:
              if link.getChild() == removal: result.append(link)
          return result

      def unlinkAnnotation(self, removal, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          toRemove = self.findOriginalFileAnnotationLink(removal)
          for next in toRemove:
              self.removeOriginalFileAnnotationLinkFromBoth( next, True )

      def removeOriginalFileAnnotationLinkFromBoth(self, link, bothSides, current = None):
          self.errorIfUnloaded()
          if not self._annotationLinksLoaded: self.throwNullCollectionException("annotationLinksSeq")
          self._annotationLinksSeq.remove( link )

      def linkedAnnotationList(self, current = None):
          self.errorIfUnloaded()
          if not self.annotationLinksLoaded: self.throwNullCollectionException("AnnotationLinks")
          linked = []
          for link in self._annotationLinksSeq:
              linked.append( link.getChild() )
          return linked

      def unloadName(self, ):
          self._nameLoaded = False
          self._name = None;

      def getName(self, current = None):
          self.errorIfUnloaded()
          return self._name

      def setName(self, _name, current = None, wrap=False):
          self.errorIfUnloaded()
          if wrap and self._field_info.name.wrapper is not None:
              if _name is not None:
                  _name = self._field_info.name.wrapper(_name)
          self._name = _name
          pass


      def ice_postUnmarshal(self):
          """
          Provides additional initialization once all data loaded
          """
          pass # Currently unused


      def ice_preMarshal(self):
          """
          Provides additional validation before data is sent
          """
          pass # Currently unused

      def __getattr__(self, name):
          import __builtin__
          """
          Reroutes all access to object.field through object.getField() or object.isField()
          """
          if "_" in name:  # Ice disallows underscores, so these should be treated normally.
              return object.__getattribute__(self, name)
          field  = "_" + name
          capitalized = name[0].capitalize() + name[1:]
          getter = "get" + capitalized
          questn = "is" + capitalized
          try:
              self.__dict__[field]
              if hasattr(self, getter):
                  method = getattr(self, getter)
                  return method()
              elif hasattr(self, questn):
                  method = getattr(self, questn)
                  return method()
          except:
              pass
          raise AttributeError("'%s' object has no attribute '%s' or '%s'" % (self.__class__.__name__, getter, questn))

      def __setattr__(self, name, value):
          """
          Reroutes all access to object.field through object.getField(), with the caveat
          that all sets on variables starting with "_" are permitted directly.
          """
          if name.startswith("_"):
              self.__dict__[name] = value
              return
          else:
              field  = "_" + name
              setter = "set" + name[0].capitalize() + name[1:]
              if hasattr(self, field) and hasattr(self, setter):
                  method = getattr(self, setter)
                  return method(value)
          raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, setter))

_omero_model.OriginalFileI = OriginalFileI
