# Project Overview
## Introduction
This project involves analyzing student performance utilizing tools such as Excel, Power Query, Power BI, and DAX.

This markdown document will serve to chronicle my process, assumptions, methodology, and any DAX or M code utilized. It will mainly take the form of a log detailing the steps undertaken, supplemented by additional commentary and code throughout the process.

## Objective
The goals of this project include:
- Gaining insights into the factors affecting student performance.
- Developing a report that facilitates easy data comprehension for users.

## Data
The dataset I will be utilizing is publicly available on Kaggle and can be accessed via the following link: [Kaggle Dataset](https://www.kaggle.com/datasets/rabieelkharoua/students-performance-dataset).

A data dictionary detailing the original structure of the dataset is provided below.

| Category               | Column             | Description                                                                                      |
|------------------------|--------------------|--------------------------------------------------------------------------------------------------|
| Demographic Details    | StudentID          | A unique identifier assigned to each student (1001 to 3392).                                    |
|                        | Age                | The age of the students ranges from 15 to 18 years.                                              |
|                        | Gender             | Gender of the students, where 0 represents Male and 1 represents Female.                         |
|                        | Ethnicity          | The ethnicity of the students, coded as follows:                                                 |
|                        |                    | - 0: Caucasian                                                                                  |
|                        |                    | - 1: African American                                                                           |
|                        |                    | - 2: Asian                                                                                       |
|                        |                    | - 3: Other                                                                                       |
| Parental Education     | ParentalEducation  | The education level of the parents, coded as follows:                                            |
|                        |                    | - 0: None                                                                                        |
|                        |                    | - 1: High School                                                                                |
|                        |                    | - 2: Some College                                                                               |
|                        |                    | - 3: Bachelor's                                                                                 |
|                        |                    | - 4: Higher                                                                                     |
| Study Habits           | StudyTimeWeekly    | Weekly study time in hours, ranging from 0 to 20.                                                |
|                        | Absences           | Number of absences during the school year, ranging from 0 to 30.                                  |
|                        | Tutoring           | Tutoring status, where 0 indicates No and 1 indicates Yes.                                        |
| Parental Involvement   | ParentalSupport    | The level of parental support, coded as follows:                                                  |
|                        |                    | - 0: None                                                                                        |
|                        |                    | - 1: Low                                                                                         |
|                        |                    | - 2: Moderate                                                                                    |
|                        |                    | - 3: High                                                                                        |
|                        |                    | - 4: Very High                                                                                   |
| Extracurricular        | Extracurricular    | Participation in extracurricular activities, where 0 indicates No and 1 indicates Yes.            |
|                        | Sports             | Participation in sports, where 0 indicates No and 1 indicates Yes.                                 |
|                        | Music              | Participation in music activities, where 0 indicates No and 1 indicates Yes.                        |
|                        | Volunteering       | Participation in volunteering, where 0 indicates No and 1 indicates Yes.                             |
| Academic Performance   | GPA                | Grade Point Average on a scale from 2.0 to 4.0, influenced by study habits, parental involvement, and extracurricular activities. |
|                        | GradeClass         | Classification of students grade based on their GPA, coded as follows:                              |
|                        |                    | - 0: 'A' (GPA >= 3.5)                                                                               |
|                        |                    | - 1: 'B' (3.0 <= GPA < 3.5)                                                                               |
|                        |                    | - 2: 'C' (2.5 <= GPA < 3.0)                                                                                 |                                                                             |
|                        |                    | - 3: 'D' (2.0 <= GPA < 2.5)                                                                               |
|                        |                    | - 4: 'F' (GPA < 2.0)                                                                               |
                                                

## Project Overview
Here's my approach to executing the project:
- Pre-process the data
- Explore the data
- Analyze the data
- Visualize and report

The project lacks a specific objective regarding recommendations. Its purpose is exploratory, aiming to understand students' study habits and the impact of various external factors on them.

# Pre-Processing
I will begin by importing the data into the Power BI environment for preprocessing. The data is in an excellent state for machine learning, with all variables encoded and feature-engineered. To demonstrate my data manipulation skills using M and DAX, I will reverse-engineer the features, converting encoded variables back into text for straightforward visualization and encoding.

- Connect to the data source and load data into Power BI
- Examine the data in the Power Query editor
- Finish and load the data

Next, I will convert the column values into text to simplify analysis. I will utilize Power Query's M language, specifically the 'Column From Examples' feature, by entering the corresponding text values, which is the fastest and simplest method for this task. Moreover, should the dataset receive updates, the changes would apply automatically.

- Create new gender column where 0 becomes 'Male' and 1 becomes 'Female'
```
= Table.AddColumn(#"Changed Type", "n_Gender", each if [Gender] = 1 then "Female" else if [Gender] = 0 then "Male" else null, type text)
```
- Create updated ethnicity column
```
= Table.AddColumn(#"Added Conditional Column", "n_Ethnicity", each if [Ethnicity] = 0 then "Caucasian" else if [Ethnicity] = 2 then "Asian" else if [Ethnicity] = 1 then "African American" else if [Ethnicity] = 3 then "Other" else null, type text)
```
- Create updated parental education column
```
= Table.AddColumn(#"Added Conditional Column1", "n_ParentalEducation", each if [ParentalEducation] = 2 then "Some College" else if [ParentalEducation] = 1 then "High School" else if [ParentalEducation] = 3 then "Bachelor's" else if [ParentalEducation] = 0 then "None" else if [ParentalEducation] = 4 then "Higher" else null, type text)
```
- Create updated tutoring column
```
= Table.AddColumn(#"Added Conditional Column2", "n_Tutoring", each if [Tutoring] = 1 then "Yes" else if [Tutoring] = 0 then "No" else null, type text)
```
- Create updated parental support column
```
= Table.AddColumn(#"Added Conditional Column3", "n_ParentalSupport", each if [ParentalSupport] = 2 then "Moderate" else if [ParentalSupport] = 1 then "Low" else if [ParentalSupport] = 3 then "High" else if [ParentalSupport] = 4 then "Very High" else if [ParentalSupport] = 0 then "None" else null, type text)
```
- Create updated extracurricular column
```
= Table.AddColumn(#"Added Conditional Column4", "n_Extracurricular", each if [Extracurricular] = 0 then "No" else if [Extracurricular] = 1 then "Yes" else null)
```
- Create updated sports column
```
= Table.AddColumn(#"Added Conditional Column5", "n_Sports", each if [Sports] = 0 then "No" else if [Sports] = 1 then "Yes" else null, type text)
```
- Create updated music column
```
= Table.AddColumn(#"Added Conditional Column6", "n_Music", each if [Music] = 1 then "Yes" else if [Music] = 0 then "No" else null, type text)
```
- Create updated volunteering column
```
= Table.AddColumn(#"Added Conditional Column7", "n_Volunteering", each if [Volunteering] = 0 then "No" else if [Volunteering] = 1 then "Yes" else null, type text)
```
- Create updated grade class column
```
= Table.AddColumn(#"Added Conditional Column8", "n_GradeClass", each if [GradeClass] = 0 then "A" else if [GradeClass] = 1 then "B" else if [GradeClass] = 2 then "C" else if [GradeClass] = 3 then "D" else if [GradeClass] = 4 then "F" else null)
```
- Delete old encoded columns, leaving a couple to help order the columns
```
= Table.RemoveColumns(#"Added Conditional Column9",{"Gender", "Ethnicity", "Tutoring", "Extracurricular", "Sports", "Music", "Volunteering"})
```
- Rename columns
```
= Table.RenameColumns(#"Removed Columns",{{"ParentalEducation", "ParentalEducation_Order"}, {"ParentalSupport", "ParentalSupport_Order"}, {"GradeClass", "GradeClass_Order"}})
```
```
= Table.RenameColumns(#"Renamed Columns1",{{"n_Gender", "Gender"}, {"n_Ethnicity", "Ethnicity"}, {"n_ParentalEducation", "ParentalEducation"}, {"n_Tutoring", "Tutoring"}, {"n_ParentalSupport", "ParentalSupport"}, {"n_Extracurricular", "Extracurricular"}, {"n_Sports", "Sports"}, {"n_Music", "Music"}, {"n_Volunteering", "Volunteering"}, {"n_GradeClass", "GradeClass"}})
```

Now that all the columns are decoded, I will check and correct data types as well as format the columns into the desired format.

- Change the data types
```
= Table.TransformColumnTypes(#"Renamed Columns",{{"Extracurricular", type text}, {"GradeClass", type text}})
```

Before proceeding, I will swiftly go through and inspect the dropdown filters on all columns in the Power Query editor to ensure there are no nulls or undesired values.

- Check the range of values in each columns

All preparations are complete and we are ready to commence the analysis.

- Close and apply the query

# Data Exploration

Here, I will be exploring the data in Power BI using visuals and tables to gather insights for my report. This section will contain notes for review, allowing me to decide what to include in my final report.

## Study Time & GPA
- Initially, I aim to examine the effect of study time on GPA using trendlines and determine the coefficient. To do this, I will use the following DAX code to create a calculated measure:
```
studytime coeff = 
    VAR __muX = AVERAGE('Student_performance'[StudyTimeWeekly])
    VAR __muY = AVERAGE('Student_performance'[GPA])
    VAR __numerator = SUMX(Student_performance, (Student_performance[StudyTimeWeekly] - __muX) * (Student_performance[GPA] - __muY))
    VAR __denominator = SQRT(SUMX(Student_performance, (Student_performance[StudyTimeWeekly] - __muX)^2) * SUMX(Student_performance, (Student_performance[GPA] - __muY)^2))
RETURN
    __numerator / __denominator
```
  - Coefficient: 0.18
  - The small coefficient of 0.18 indicates a weak positive correlation. Students who study more tend to have marginally higher GPAs, but the impact is not significant. It suggests that other factors may have a greater influence on GPA.

## Average GPA by Gender
- Female: 1.89
- Male: 1.92

The negligible difference of 0.03 is so minor that it should not be considered significant.

## Average GPA by Ethnicity
The GPA range for each ethnicity, from 1.88 to 1.95, shows a variance of 0.07. This difference is so slight that it should not be considered a significant factor.

## Average GPA by Parental Support
- None: 1.54
- Low: 1.76
- Moderate: 1.88
- High: 2.04
- Very High: 2.19

This presents a more substantial difference compared to the other factors examined. While it may not be the sole predictor of a student's GPA, it appears to be a contributing factor.

## Average GPA by Number of Absences
I created a column chart with absences on the X-axis and Average GPA on the Y-axis, which shows a very clear downward trend as absences increase.

I will quickly calculate the coefficient for this to understand the relationship better.
```
Abscences Coeff = 
    VAR __muX = AVERAGE('Student_performance'[Absences])
    VAR __muY = AVERAGE('Student_performance'[GPA])
    VAR __numerator = SUMX(Student_performance, (Student_performance[Absences] - __muX) * (Student_performance[GPA] - __muY))
    VAR __denominator = SQRT(SUMX(Student_performance, (Student_performance[Absences] - __muX)^2) * SUMX(Student_performance, (Student_performance[GPA] - __muY)^2))
RETURN
    __numerator / __denominator
```
- Coefficient: -0.92
  - This represents a very high negative correlation, indicating that for every single absence, the GPA tends to decrease by 0.92 points, which is a significant impact.
  - Caveat: It's important to note that this does not imply causation, and other factors may affect a student's GPA. However, there is a strong correlation with overall GPA.

## Tutoring and Average GPA
- With Tutoring: 2.11
- Without Tutoring: 1.82

This data suggests a modest increase in GPA due to tutoring, indicating that tutoring tends to lead to a higher GPA. A scatter plot will be used for further observation.

## Parental Support and GPA
A line chart reveals a marked upward trend in average GPA with increased parental support. The coefficient will be calculated next.
```
ParentalSupport Coeff = 
    VAR __muX = AVERAGE('Student_performance'[ParentSupport_Order])
    VAR __muY = AVERAGE('Student_performance'[GPA])
    VAR __numerator = SUMX(Student_performance, (Student_performance[ParentSupport_Order] - __muX) * (Student_performance[GPA] - __muY))
    VAR __denominator = SQRT(SUMX(Student_performance, (Student_performance[ParentSupport_Order] - __muX)^2) * SUMX(Student_performance, (Student_performance[GPA] - __muY)^2))
RETURN
    __numerator / __denominator
```
Coefficient: 0.19
- This indicates a positive relationship between parental support and GPA. When considering the overall picture, the GPA increases by approximately 0.19 points as parental support rises by one level. However, when examining the average GPA, the scenario is quite different. This suggests that while other factors also influence GPA, parental support nonetheless plays a role.

## Parent Education Level and Student GPA
Analysis of charts and tables shows no discernible pattern between the level of parental education and a student's GPA. This implies that a parent's higher education does not significantly affect a student's academic performance.

## Student Age and GPA
There appears to be no significant variation in GPA across different age groups, indicating that age does not greatly affect academic performance.

## Extracurricular Activities and Volunteering
Examination of how these variables affect a student's GPA shows no definitive trends.

## Recap of Exploration
After exploring how various factors affect the average GPA, I have identified three elements that do make a positive impact on a student's GPA:
- Parental support
- Number of absences
- Tutoring

These are the aspects I will emphasize in my report, underscoring that these are the areas schools and parents should concentrate on to enhance student performance.

# Visualize and Report
I will next construct a report that delves into the data and highlights the key metrics that affect a student's academic performance. This section will not contain extensive documentation, as the report is intended to be viewed by the user alongside this documentation.

# Summary of Findings
An examination of the data revealed three key factors that contribute to a student's academic success. Interestingly, study time appears to have a minimal impact on achieving a higher GPA. Instead, it is linked to support and attendance. My report and findings indicate correlation, not causation, meaning that while these characteristics are common among students with higher GPAs, they do not guarantee academic success.
The three most significant factors are:
- Attendance: GPA decreases by an average of 0.10 points for each absence.
- Academic Support: Students enrolled in tutoring programs have an average GPA that is 0.30 points higher.
- Parental Support: Students with minimal or no parental support have an average GPA that is 0.30 points lower than those with moderate to very high parental support.

These factors should be a focus for both parents and schools. Promoting parental involvement, making tutoring more accessible, and ensuring students have the resources to maintain high attendance can pave the way for academic success.







**All code, analysis, and visualizations were performed by Joshua Plunkett.*









