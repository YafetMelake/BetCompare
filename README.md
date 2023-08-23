# BetCompare: Sports Betting Odds Comparison System

Welcome to BetCompare, a sports betting odds comparison system that shows users the best up-to-date odds information for football matches. This README document provides an in-depth understanding of the technical flow and architecture of the BetCompare system.

## Table of Contents

- [Overview](#overview)
- [Backend Code](#backend-code)
  - [Data Retrieval and Storage](#data-retrieval-and-storage)
  - [Backend Functions](#backend-functions)
  - [Database Schema](#database-schema)
- [Flask Web Application](#flask-web-application)
  - [Web Application Flow](#web-application-flow)
  - [Web Application Features](#web-application-features)
- [Scheduled Data Refresh](#scheduled-data-refresh)
- [Conclusion](#conclusion)

## Overview

BetCompare is a system that provides users with an insight into which betting company provides the best odds for the same match. The system consists of a backend module responsible for fetching data, processing it, and storing it in a database, while the frontend utilises a Flask web application to display this data to users in a user-friendly format.

## Backend Code

The backend of BetCompare focuses on fetching data from an external API, processing it, and storing it in a SQLite database. Due to the fact that I am limited by the data the API provides and also limited by the amount of API calls I can make, the system provides the insights into whatever football match data I receive.

### Data Retrieval and Storage

1. **API Integration**: BetCompare communicates with the Odds API to retrieve odds, bookmaker, and match data for soccer matches.

2. **Database Storage**: The fetched data is organised into multiple tables within a SQLite database. These tables include:
   - `ODDSTABLE`: Stores odds data for matches, bookmakers, and teams. This table was used in order to allow me to verify and check the data in the other tables mapped correctly to eachother.
   - `BOOKMAKERS`: Contains bookmaker names and unique IDs.
   - `Matches`: Holds match information such as date, team playing against eachother, and description.
   - `PRICE`: Maps bookmakers and matches to their respective odds data.

### Backend Functions

BetCompare's backend includes the following functions to facilitate data processing and storage:

- `sports_odds()`: Retrieves odds data through the Odds API and returns the response in JSON format.
- `save_sports(key, sportsdbfile)`: Processes and saves odds data for matches, bookmakers, and teams in the `ODDSTABLE`.
- `bookmakers_table(sportsdbfile, response_data)`: Populates the `BOOKMAKERS` table with bookmaker names.
- `matches_table(sportsdbfile, response_data)`: Fills the `Matches` table with match information.
- `price_table(sportsdbfile, response_data)`: Stores odds data in the `PRICE` table, linking bookmakers and matches.
- `sportssoddss(sportsdbfile)`: Calls the above functions to fetch and store sports odds data.

### Database Schema

BetCompare's SQLite database employs a structured schema for efficient data storage and retrieval. The tables are interconnected to ensure seamless integration.

## Flask Web Application

The frontend of BetCompare is a responsive Flask web application that showcases the odds data stored in the database.

### Web Application Flow

1. **Database Query**: The Flask app queries the SQLite database to fetch odds and match information.

2. **Grouping by Leagues**: The data is organised by leagues, and matches are grouped under their respective leagues.

3. **Template Rendering**: The Flask app renders an HTML template to present the grouped matches and odds data.

### Web Application Features

- **Accordion Interface**: Leagues are displayed as collapsible cards using an accordion interface. Users can expand and collapse each league to view its matches.
- **Match Information**: Matches are presented with details including home and away teams, odds, and bookmaker names. Bookmaker names are linked to their respective websites which provides users with an efficient way to access the bookmakers' platforms for placing bets.
- **Styling**: Bootstrap is employed to ensure a responsive and visually appealing design for a seamless user experience.

## Scheduled Data Refresh

BetCompare's `setup_initial_data()` function in `main.py` ensures that odds data remains current by periodically updating the database. This function can be scheduled to run at specific intervals using tools like `cron` jobs or task schedulers, maintaining the accuracy of odds information.

## Conclusion

BetCompare offers transparency within the betting industry, giving users the information they need to make informed decisions. Its architecture ensures efficient data processing, seamless integration, and dynamic data presentation. The combination of backend data handling and frontend web application design establishes BetCompare as a reliable source for up-to-date sports betting odds information.
