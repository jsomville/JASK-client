import json
import math

file_source = 'JASK-client/src/data/map.json'
file_dest = 'JASK-client/src/data/new_map.json'
with open(file_source) as f:
    data = json.load(f)
    
for ss in data['SolarSystems']:
    #For every planets
    max = 0
    for planet in ss['objects']:
        
        if planet["type"] == "planet":
            #Fix Period
            period = int(planet["period"])
            planet["angle"] = period % 360
                

            #Get Max distance
            dist = planet["distance"] 
            if dist > max:
                max = dist

    ss["map_size"] = (max * 2 + 200, max *2 + 200)
    
    #Convert Period & distance into points
    for planet in ss['objects']:
        rad_angle = math.radians(planet["angle"])
        x = round(max + planet["distance"]  * math.cos(rad_angle))
        y = round(max + planet["distance"]  * math.sin(rad_angle))
        
        planet["position"] = (x,y)
        
            
print(json.dumps(data, indent=2))

with open(file_dest, 'w') as f:
    json.dump(data, f, indent=2)