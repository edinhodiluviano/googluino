# googluino
"Buscapé" para componentes eletronicos

### Instalação (com python 3.6 e pip em linux)
```bash
# Clonar o repositório:
git clone git@github.com:edinhodiluviano/googluino.git
# Criar e ativar o virtualenv:
cd googluino
virtualenv venv -p python3.6
source venv/bin/activate
# Instalar dependencias
pip install -r requirements.txt
```

### Uso
```bash
cd googluino
source venv/bin/activate
python main.py arduino
```
O programa vai pesquisar os sites contidos no arquivo metadata.py
Printar um resumo dos resultados, como abaixo
E salvar um arquivo .csv com os resultados

###### Exemplo de resultados
```bash
n: 0	query: arduino	site: newport	items: 12
n: 1	query: arduino	site: mscnbrasil	items: 0
n: 2	query: arduino	site: hperobotica	items: 48
n: 3	query: arduino	site: multcomercial	items: 29
n: 4	query: arduino	site: filipeflop	items: 64
n: 5	query: arduino	site: baudaeletronica	items: 16
Searched 5 sites. Found 169 results. Results saved to results_20181008_1025_arduino.csv
```
