from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

class DuoViewModel(BaseModel):
    word1: str
    word2: str
    output_path: str

def create_duoview_model(word1: str, word2: str, output_path: str) -> str:
    def add_variable(name, value):
        return f"-D {name}='\"{value}\"'"

    openscad_path = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
    program_path = "/Users/davidhaas/projects/cad-generation/names.scad"
    command = (
        f"{openscad_path} -o '{output_path}' '{program_path}' "
        + f'{add_variable("name1",word1)} {add_variable("name2",word2)}'
    )
    print(command)
    os.system(command)
    return output_path


@app.post("/create_model/")
async def create_model(data: DuoViewModel):
    try:
        stl_path = create_duoview_model(data.word1, data.word2, data.output_path)
        return {"message": "Successfully created model", "stl_path": stl_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    output_path = os.path.join(os.getcwd(), "test.stl")
    stl_path = create_duoview_model("DAVE", "HAAS", output_path)
    print(stl_path)
