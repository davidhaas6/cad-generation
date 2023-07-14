from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from random import randint
import os

static_file_dir = '/Users/davidhaas/projects/cad-gen-site/cad-server/static'
static_route = "/static"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DuoViewModel(BaseModel):
    word1: str
    word2: str


def create_duoview_model(word1: str, word2: str) -> str:
    def add_variable(name, value): return f"-D {name}='\"{value}\"'"
    def get_file_id(): return hex(randint(1,1e20))[2:]

    word1 = word1.upper()
    word2 = word2.upper()

    file_path = f"{get_file_id()}.stl"
    openscad_path = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
    program_path = "/Users/davidhaas/projects/cad-gen-site/cad-server/names.scad"
    command = (
        f"{openscad_path} -o '{os.path.join(static_file_dir, file_path)}' '{program_path}'"
        + f' {add_variable("name1",word1)} {add_variable("name2",word2)}'
    )
    print(command)
    os.system(command)
    return os.path.join(static_route,file_path)

@app.get("/")
def landing():
    return 'Hello!'


@app.post("/create_model/")
async def create_model(data: DuoViewModel):
    try:
        print("Recieved data:",data)
        stl_path = create_duoview_model(data.word1, data.word2)
        print(f'{stl_path} created')
        return {"message": "Successfully created model", "output_path": stl_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.mount(static_route, StaticFiles(directory=static_file_dir), name="static")

if __name__ == "__main__":
    stl_path = create_duoview_model("DAVE", "HAAS")
    print(stl_path)
