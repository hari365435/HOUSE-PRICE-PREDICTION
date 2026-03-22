from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import joblib
import pandas as pd
model=joblib.load("ml_model.pkl")
print(type(model))
app=FastAPI(debug=True)
tier1=['Ahmedabad','Amritsar','Bangalore','Bhilai', 'Bhopal', 'Bhubaneswar',
 'Bilaspur' ,'Chennai' ,'Coimbatore' ,'Cuttack' ,'Dehradun' ,'Dhanbad']
tier2=['Durgapur' ,'Dwarka' ,'Ernakulam', 'Faridabad', 'Gurgaon' ,'Guwahati',
 'Gwalior', 'Haridwar' ,'Howrah' ,'Hyderabad', 'Indore', 'Jaipur', 'Jalandhar']
class UserInput(BaseModel):
    bhk:Annotated[int,Field(...,description='no of bedrooms you required',)]
    propertytype:Annotated[Literal['Villa','Flat','House'],Field(...,description='type of property')]
    location:Annotated[str,Field(...,description='which city are insterested in')]
    sqft:Annotated[int,Field(...,description='approx sqft house you need')]
    
    @computed_field
    @property
    def pp(self) -> int:
        if self.propertytype =="Flat":
           return 1
        elif self.propertytype=="Villa":
           return 2
        else:
           return 3
     

    @computed_field
    @property
    def city_tier(self) ->int:
       if self.location in tier1:
          return 1
       elif self.location in tier2:
          return 2
       else:
          return 3
    

@app.post('/predict')
def total_price(data:UserInput):
    input_df=pd.DataFrame([{
        'bhk':data.bhk,
        "pp":data.pp,
        "city_tier":data.city_tier,
        "sqft":data.sqft
    }])
    prediction=model.predict(input_df)[0]
   
    return JSONResponse(status_code=200,content={'predicted_houseprice':float(prediction)})

