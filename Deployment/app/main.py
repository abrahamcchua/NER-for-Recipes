# Python Frameworks
from fastapi import FastAPI
from pydantic import BaseModel
# Own Module
from app.ner import ner_model

'''
The backend script for the project
:Date: January 23, 2023
:Author/s: 
    - Chua, Abraham <abrahamcchua@gmail.com>
'''



class Text(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
def initialize():
    return {
        "Message": "Successfully Initialized."
    }

@app.post("/extract")
def root(
    text: Text,
):
    return ner_model(text.text).get_predicted_entities() 


# if __name__ == "__main__":
#     text = """Cook pasta according to package directions. Meanwhile, in a large skillet, cook beef over medium heat until no longer pink; drain and set aside.
#     In the same skillet, cook bacon until crisp; remove with a slotted spoon to paper towels to drain. Discard drippings. Drain pasta; add to the skillet. Stir in the soup, water, beef and bacon; heat through.
#     Remove from the heat and sprinkle with cheese. Cover and let stand for 2-3 minutes or until the cheese is melted. Serve with barbecue sauce and mustard if desired. """
#     ner_model(text).get_predicted_entities()