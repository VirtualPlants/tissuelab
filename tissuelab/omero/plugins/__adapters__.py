
__all__ = []

from openalea.vpltk.catalog.factories import ObjectFactory


AdapterSpatialImageToImage5D = ObjectFactory(name='AdapterSpatialImageToImage5D', 
                          description="A sample to show adapter mechanism", 
                          category="test", 
                          interfaces=["IAdapter", "ISpatialImage", "IOmeroImage"], 
                          nodemodule="openalea.omero.adapters", 
                          nodeclass="AdapterSpatialImageToImage5D",
                          adapter_inputs = ['ISpatialImage'],
                          adapter_outputs = ['IOmeroImage'],
                          )
__all__.append('AdapterSpatialImageToImage5D')


