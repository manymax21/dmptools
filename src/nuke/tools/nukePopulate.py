#=========================================
# 
# nuke populate geo onto 3d selection 
# michael.havart@gmail.com
# 
#=========================================

import nuke
import random
        
class Populate(object):
    """
    randomly populate a given number of spheres onto
    a source object
    """
    def __init__(self):
        """
        create the python geo node and get the number of points
        of the source geo
        """
        self.pyGeo = nuke.createNode("PythonGeo", inpanel = False)
        self.numPList = self.pyGeo['geo_select'].getGeometry()[0].points()
        self.numP = len(self.numPList)
        
    def UI(self):
        """
        create UI that ask for the number of objects
        """
        panel = nuke.Panel('How many copies ?')
        panel.addSingleLineInput('The source object has '+str(self.numP)+' points:', '')
        val = panel.show()
        if val:
            text = panel.value('The source object has '+str(self.numP)+' points:')
            try:
                value = int(text)
                return value
            except ValueError:
                nuke.message("Please type a int value !")
                raise
        else:
            self.clean()
            raise UserWarning("abort by the user...")
            
    def populate(self, number):
        """
        from the number of points given by the user,
        create a sphere on a random point of the source object
        """
        # randomize points
        numPList = range(self.numP)
        random.shuffle(numPList)
        numP = numPList[1:number+1]
        objects = []

        for p in numP:
            point =  self.numPList[p]   
            # create sphere
            sphere = nuke.createNode("Sphere", inpanel = False)
            sphere['uniform_scale'].setValue(.2)
            sphere['rows'].setValue(8)
            sphere['columns'].setValue(8)
            # move the sphere
            sphere['translate'].setValue(point)
          
            objects.append(sphere)
    
        # unselect all nodes
        [node.knob('selected').setValue(False) for node in nuke.allNodes()]

        # create scene
        if objects:
            for node in objects:
                node['selected'].setValue(True)
            scene = nuke.createNode("Scene")
            
            return objects, scene
            
    def clean(self):
        """
        delete the python geo node
        """
        nuke.delete(self.pyGeo)

def main():
    source = nuke.selectedNode()
    goodGeo = ["DisplaceGeo",
                "TransformGeo",
                "UVProject",
                "MergeGeo",
                "Normals",
                "ProcGeo",
                "RadialDistort",
                "Trilinear",
                "CrosstalkGeo",
                "GeoSelect",
                "LookupGeo",
                "LogGeo",
                "WriteGeo",
                "WriteGeo2",
                "ReadGeo",
                "ReadGeo2",
                "Sphere",
                "Sphere2",
                "Cube",
                "Cube2",
                "Cylinder",
                "Cylinder2",
                "Card",
                "Card2",
                "PythonGeo",
                "GiggleGeoLoader",
                ]
                
    if source.Class() in goodGeo:
        populate = Populate()
        number = populate.UI()
        if number <= populate.numP:
            populate.populate(number)
            populate.clean()
        else:
            nuke.message('Not enough points in the source object:\n'+str(populate.numP))
    else:
        nuke.message('Please select a 3d object')
        
if __name__ == "__main__":
    main()