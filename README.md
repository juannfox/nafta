# nafta

**Python-based** API that retrieves *gas prices in Argentina*, from official listings.

<p align="left">
  <img src="./images/GasStation-Dall-e-2.png" width="400" title="Gas Station, Digital Art, by Dall·E-2">
  <br/>
  <span>Gas Station (Digital Art), by </span><a href="https://openai.com/product/dall-e-2">Dall·E-2</a>
</p>

## Getting started

## Tooling

- Python 3.10 or newer
- pip3

### Workspace

´´´shell
# Setup a virtual environment, load it 
# and install pip packages
source ./load_environment.sh
´´´

### Linting

´´´shell
# Run all the linting tools
./lint.sh
´´´

### Running the API

´´´shell
cd python
uvicorn main:app --reload
´´´

## Source

The gas prices are fetched from *Argentina's* government API, specifically the Dataset [energia-precios-surtidor---resolucion-3142016](https://datos.gob.ar/dataset/energia-precios-surtidor---resolucion-3142016). After some processing of the response, we get an URL pointing towards a CSV file containing gas prices for every gas station in the country.

Structure for the response:

- DatasetResponse: JSON metadata for Dataset
  - DatasetResurce: JSON metadata for the target file
    - URL to csv file
