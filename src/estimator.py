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
  impact["hospitalBedsByRequestedTime"] = int(0.35 * data.get("totalHospitalBeds") - impact["severeCasesByRequestedTime"])
  severeImpact["hospitalBedsByRequestedTime"] = int(0.35 * data.get("totalHospitalBeds") - severeImpact["severeCasesByRequestedTime"])

  # estimate number of severe cases that will require ICU care
  impact["casesForICUByRequestedTime"] = int(0.05 * impact["infectionsByRequestedTime"])
  severeImpact["casesForICUByRequestedTime"] = int(0.05 * severeImpact["infectionsByRequestedTime"])

  # estimate number of severe positive cases that will require ventilators
  impact["casesForVentilatorsByRequestedTime"] = int(0.02 * impact["infectionsByRequestedTime"])
  severeImpact["casesForVentilatorsByRequestedTime"] = int(0.02 * severeImpact["infectionsByRequestedTime"])

  # estimate how much money the economy will lose daily
  impact["dollarsInFlight"] = int((impact["infectionsByRequestedTime"] * data.get("region").get("avgDailyIncomePopulation") * data.get("region").get("avgDailyIncomeInUSD")) * convertedDays)
  severeImpact["dollarsInFlight"] = int((severeImpact["infectionsByRequestedTime"] * data.get("region").get("avgDailyIncomePopulation") * data.get("region").get("avgDailyIncomeInUSD")) * convertedDays)

  return estimate

data = {
        "region": {
          "name": "Africa",
          "avgAge": 19.7,
          "avgDailyIncomeInUSD": 4,
          "avgDailyIncomePopulation": 0.73
        },
        "periodType": "days",
        "timeToElapse": 38,
        "reportedCases": 2747,
        "population": 92931687,
        "totalHospitalBeds": 678874
}

print(estimator(data))