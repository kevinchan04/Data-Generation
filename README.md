# Data Generate

## CAD-60 Dataset

### To genrate json file

Open the file `generate_json.ipynb` in your jupyter-notebook. Befoer running the code, you have to change the default location which stores your dataset in code 
**line 2**.
```
data_dicts = r"./"
```

### Dictionary structure
```
{
    "a str of ten-digit integer" : {
        "person_ID": int
        "folder_path": image folder,
        "action_label": string of action label,
        "frames": {
            "ID" : {
                "ROI" : {
                    "Joint ID" : {
                        "orin" : list,
                        "CONF" : int
                    }
                }
                "P" : {
                    "Joint ID" : {
                        "coor" : list,
                        "CONF" : int
                    }
                }
            }
        }
    }
}
```
* "a str of ten-digit integer" is a string of code which represends a specific image folder. It is corresponding to one activity.
* "person_ID" is an integer between 1,2,3,4 due to the data were collected from four person.
* "folder_path" is the location of image folder. In CAD-60 dataset, RGB and depth images are sotred in one folder. The folder code is linked to *a str of ten0digit interger*.
* "action_label" refers to the action that it belongs to.
* "frames" stores all data in *"folder_path"*, you can search by image **ID**.
* "ID" is the interger begins from 1. It is refers to the image ID.
* "ROI" is orientation of the joints.
* "Joint ID" is an interger begins from 0, end in 10. In CAD dataset, there are only 11 joints include the orientation.
* "orin" is a list with 9 elements.
* "CONF" is the  boolean confidence value (0 or 1).
* "P" refers to joint points.
* "coor" is a list with 3 elements, which are **x,y,z**. The origin of the corridinate system is at the sensor.
