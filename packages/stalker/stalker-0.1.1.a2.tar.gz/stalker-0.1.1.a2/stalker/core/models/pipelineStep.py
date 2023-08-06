#-*- coding: utf-8 -*-



from stalker.core.models import entity







########################################################################
class PipelineStep(entity.Entity):
    """A PipelineStep object represents the general pipeline steps which are
    used around the studio. A couple of examples are:
    
      * Design
      * Model
      * Rig
      * Fur
      * Shading
      * Previs
      * Match Move
      * Animation
      
      etc.
    
    Doesn't add any new parameter for its parent class.
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(PipelineStep, self).__init__(**kwargs)





