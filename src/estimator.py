def convertToDays(input, inputType):
  if inputType == "days":
    return input
  elif inputType == "weeks":
    return input * 7
  elif inputType == "months":
    return input * 30

def estimator(data):
  # initialize the required variables
  impact = {}
  severeImpact = {}
  estimate = {"data": data,
              "impact": impact,
              "severeImpact": severeImpact}
  convertedDays = convertToDays(data.get("timeToElapse"), data.get("periodType"))

  # calculate the currently infected people
  impact["currentlyInfected"] = data.get("reportedCases") * 10
  severeImpact["currentlyInfected"] = data.get("reportedCases") * 50

  # calculate the estimated number of people infected in the future
  impact["infectionsByRequestedTime"] = impact["currentlyInfected"] * (2 ** (convertedDays // 3))
  severeImpact["infectionsByRequestedTime"] = severeImpact["currentlyInfected"] * (2 ** (convertedDays // 3))

  # estimate number of severe cases that will require hospitalization
  impact["severeCasesByRequestedTime"] = int(0.15 * impact["infectionsByRequestedTime"])
  severeImpact["severeCasesByRequestedTime"] = int(0.15 * severeImpact["infectionsByRequestedTime"])

  # calculate the number of hospital beds available
  impact["hospitalBedsByRequestedTime"] = data.get("totalHospitalBeds") - impact["severeCasesByRequestedTime"]
  severeImpact["hospitalBedsByRequestedTime"] = data.get("totalHospitalBeds") - severeImpact["severeCasesByRequestedTime"]

  return estimate

data = {
        "region": {
          "name": "Africa",
          "avgAge": 19.7,
          "avgDailyIncomeInUSD": 5,
          "avgDailyIncomePopulation": 0.71
        },
        "periodType": "days",
        "timeToElapse": 58,
        "reportedCases": 674,
        "population": 66622705,
        "totalHospitalBeds": 1380614
}

print(estimator(data))