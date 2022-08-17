# Monkeypox cases map for Verywell Health

This repository runs the YAML file `cdc_monkeypox_runner.yml` in the .github/workflows directory.

The YAML file is run every weekday just after 19:00 UTC and triggers the python script `update_monkeypox_cases.py` to collect the latest Monkeypox case data from the [Centers for Disease Control and Prevention](https://www.cdc.gov/poxvirus/monkeypox/response/2022/us-map.html) and uses it to update the Datawrapper case map that is present on [Verywell health's](https://www.verywellhealth.com/) Monkeypox cases article.

The python script also outputs a CSV file `cdc_monkeypox_cases.csv` in the `visualizations` folder that is sent to the [Datawrapper](https://www.datawrapper.de/) charts via the [Datawrapper API](https://developer.datawrapper.de/reference/introduction) and also commited to the repository.