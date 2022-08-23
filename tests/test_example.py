from pathlib import Path
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter

from covidnet_meta import parser, main, DISPLAY_TITLE
import json

def test_main(mocker, tmp_path: Path):
    """
    Simulated test run of the app.
    """
    inputdir = tmp_path / 'incoming'
    outputdir = tmp_path / 'outgoing'
    inputdir.mkdir()
    outputdir.mkdir()

    d_dummyPrediction = {
        "**DISCLAIMER**": "Do not use this prediction for self-diagnosis. You should check with your local authorities for the latest advice on seeking medical assistance.",
        "prediction": "Normal",
        "COVID-19": "1.3288779e-06",
        "Pneumonia": "9.121393e-06",
        "Normal": "0.9999895"
    }
    json_obj = json.dumps(d_dummyPrediction, indent = 4)
    with open("%s/prediction-default.json" % inputdir, "w") as outfile:
        outfile.write(json_obj)

    options = parser.parse_args(['--prediction', 'prediction-default.json'])
    options.inputdir = inputdir
    options.outputdir = outputdir

    mock_print = mocker.patch('builtins.print')
    main(options, inputdir, outputdir)

    expected_output_file = outputdir / 'prediction-default.json'
    assert expected_output_file.exists()
