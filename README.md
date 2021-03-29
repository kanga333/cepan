# cepan

[![test](https://github.com/kanga333/cepan/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/kanga333/cepan/actions/workflows/test.yml)
[![lint](https://github.com/kanga333/cepan/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/kanga333/cepan/actions/workflows/lint.yml)
[![Code style: black](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Retrieves data from aws cost explore as a pandas dataframe.

Main features
- Support for input with type hints
- Retrieving results as pandas.Dataframe

## Installation

```
pip install cepan
```

## Usage

```python
from datetime import datetime

import cepan as ce

df = ce.get_cost_and_usage(
    time_period=ce.TimePeriod(
        start=datetime(2020, 1, 1),
        end=datetime(2020, 1, 2),
    ),
    granularity="DAILY",
    filter=ce.And(
        [
            ce.Dimensions(
                "SERVICE",
                ["Amazon Simple Storage Service", "AmazonCloudWatch"],    
            ),
            ce.Tags("Stack", ["Production"]),
        ]
    ),
    metrics=["BLENDED_COST"],
    group_by=ce.GroupBy(
        dimensions=["SERVICE", "USAGE_TYPE"],
    ),
)
print(df)
```

All paginated results will be returned as a Dataframe.

```
          Time                        SERVICE  BlendedCost
0   2020-01-01  Amazon Simple Storage Service   100.000000
1   2020-01-01               AmazonCloudWatch    10.000000
```

### List of currently supported APIs

- get_dimension_values
- get_tags
- get_cost_and_usage

## License

MIT License
