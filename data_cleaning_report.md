# Data Cleaning Report

## Overview
I identified four common issues in the dataset and implemented a cleaning pipeline to address them.

## Identified Issues
1. Missing Values: Many entries were missing values, especially in Price. I removed any rows with missing Price or Size.

2. Invalid Prices: Some prices were far outside the typical range (10% of values nearby). These were filtered out as anomalies.

3. Non-positive Prices: Rows with prices less than or equal to zero were excluded.

4. Duplicate Timestamps: Assuming each trade should be unique, I removed rows with duplicate timestamps.

## Assumptions
Invalid Prices: I used reasonable price bounds based on observed trends.

Duplicate Trades: I assumed each timestamp represents a unique trade.

## Challenges
Data Preservation: Balancing the removal of invalid data while keeping valid entries intact.

Outlier Detection: Considering the use of dynamic outlier detection rather than fixed bounds.