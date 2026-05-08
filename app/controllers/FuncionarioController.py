from main import app
from service.FuncionarioService import listar_clientes

@app.get("admin/clientes")
async def listar_cliente():
    return listar_clientes()