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
model_instance = ner_model()

@app.get("/")
def initialize():
    return {
        "Message": "Successfully Initialized."
    }

@app.post("/extract")
def root(
    text: Text,
):
    return model_instance.get_predicted_entities(text.text) 


# if __name__ == "__main__":
#     text = """Cook pasta according to package directions. Meanwhile, in a large skillet, cook beef over medium heat until no longer pink; drain and set aside.
#     In the same skillet, cook bacon until crisp; remove with a slotted spoon to paper towels to drain. Discard drippings. Drain pasta; add to the skillet. Stir in the soup, water, beef and bacon; heat through.
#     Remove from the heat and sprinkle with cheese. Cover and let stand for 2-3 minutes or until the cheese is melted. Serve with barbecue sauce and mustard if desired. """
#     ner_model(text).get_predicted_entities()

#    text = "Heat the oil in a deep, wide frying pan or casserole dish over a medium-high heat. Tip in the meatballs and cook for 5 mins, turning until browned all over. Add the onion and garlic, and fry for 8 more mins until softened. Add the ketchup, chopped tomatoes, chopped basil and 400ml water to the pan and bring to the boil. Add the spaghetti and cook for 10-12 mins, stirring occasionally. When the pasta is cooked and the sauce has reduced, season and sprinkle with the basil leaves to serve."