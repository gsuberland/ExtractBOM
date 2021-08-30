#Author-Autodesk Inc. and Graham Sutherland
#Description-Improved script to extract BOM information from active design.

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        title = 'Extract BOM'
        if not design:
            ui.messageBox('No active design', title)
            return

        # Get all occurrences in the root component of the active design
        root = design.rootComponent
        occs = root.allOccurrences
        
        # Gather information about each unique component
        bom = []
        for occ in occs:
            comp = occ.component
            jj = 0
            for bomI in bom:
                if bomI['component'] == comp:
                    # Increment the instance count of the existing row.
                    bomI['instances'] += 1
                    break
                jj += 1

            if jj == len(bom):
                # Gather any BOM worthy values from the component
                volume = 0
                bodies = comp.bRepBodies
                for bodyK in bodies:
                    if bodyK.isSolid:
                        volume += bodyK.volume
                
                # Add this component to the BOM
                bom.append({
                    'component': comp,
                    'name': comp.name,
                    'instances': 1,
                    'volume': volume
                })
        
        # Figure out how wide the columns need to be
        nameColWidth = max(25, max(len(item['name']) for item in bom) + 1)
        instancesColWidth = max(15, max(len(str(item['instances'])) for item in bom) + 1)

        # Display the BOM
        bomStr = 'Name'.ljust(nameColWidth) + 'Instances'.ljust(instancesColWidth) + 'Volume\n'
        for item in bom:
            bomStr += item['name'].ljust(nameColWidth) + str(item['instances']).ljust(instancesColWidth) + str(item['volume']) + '\n'

        ui.messageBox(bomStr, 'Bill Of Materials')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
