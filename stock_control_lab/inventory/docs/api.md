# API Documentation

## Overview

This document provides detailed information about the Laboratory Stock Control System API endpoints.

## Authentication

All API endpoints require authentication. Authentication is done using Django's built-in session authentication or token authentication.

## Base URL

All API endpoints are prefixed with `/api/v1/`.

## Endpoints

### Reagents

#### List Reagents
- **URL**: `/api/v1/reagents/`
- **Method**: `GET`
- **Description**: Retrieve a list of all reagents.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Sodium Chloride",
      "sku": "NACL-001",
      "category": 1,
      "supplier": 1,
      "min_stock_level": "100.00"
    }
  ]
  ```

#### Create Reagent
- **URL**: `/api/v1/reagents/`
- **Method**: `POST`
- **Description**: Create a new reagent.
- **Request Body**:
  ```json
  {
    "name": "Sodium Chloride",
    "sku": "NACL-001",
    "category": 1,
    "supplier": 1,
    "min_stock_level": "100.00"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Sodium Chloride",
    "sku": "NACL-001",
    "category": 1,
    "supplier": 1,
    "min_stock_level": "100.00"
  }
  ```

#### Get Reagent
- **URL**: `/api/v1/reagents/{id}/`
- **Method**: `GET`
- **Description**: Retrieve details of a specific reagent.
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Sodium Chloride",
    "sku": "NACL-001",
    "category": 1,
    "supplier": 1,
    "min_stock_level": "100.00"
  }
  ```

#### Update Reagent
- **URL**: `/api/v1/reagents/{id}/`
- **Method**: `PUT`
- **Description**: Update an existing reagent.
- **Request Body**:
  ```json
  {
    "name": "Sodium Chloride",
    "sku": "NACL-001",
    "category": 1,
    "supplier": 1,
    "min_stock_level": "150.00"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Sodium Chloride",
    "sku": "NACL-001",
    "category": 1,
    "supplier": 1,
    "min_stock_level": "150.00"
  }
  ```

### Stock Lots

#### List Stock Lots
- **URL**: `/api/v1/stock-lots/`
- **Method**: `GET`
- **Description**: Retrieve a list of all stock lots.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "reagent": 1,
      "lot_number": "NACL20250917",
      "location": 1,
      "expiry_date": "2026-09-17",
      "purchase_price": "50.00",
      "initial_quantity": "5000.00",
      "current_quantity": "5000.00"
    }
  ]
  ```

#### Create Stock Lot
- **URL**: `/api/v1/stock-lots/`
- **Method**: `POST`
- **Description**: Add a new stock lot to inventory (stock entry).
- **Request Body**:
  ```json
  {
    "reagent": 1,
    "lot_number": "NACL20250917",
    "location": 1,
    "expiry_date": "2026-09-17",
    "purchase_price": "50.00",
    "initial_quantity": "5000.00",
    "current_quantity": "5000.00"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "reagent": 1,
    "lot_number": "NACL20250917",
    "location": 1,
    "expiry_date": "2026-09-17",
    "purchase_price": "50.00",
    "initial_quantity": "5000.00",
    "current_quantity": "5000.00"
  }
  ```

### Stock Movements

#### Create Stock Movement
- **URL**: `/api/v1/stock-movements/`
- **Method**: `POST`
- **Description**: Register a new stock movement (withdrawal, discard).
- **Request Body**:
  ```json
  {
    "reagent": 1,
    "user": 1,
    "quantity": "50.00",
    "move_type": "Retirada",
    "notes": "For sample analysis B-12"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "stock_lot": 1,
    "user": 1,
    "quantity": "50.00",
    "move_type": "Retirada",
    "timestamp": "2025-09-17T10:30:00Z",
    "notes": "For sample analysis B-12"
  }
  ```

### Dashboard

#### Get Dashboard Summary
- **URL**: `/api/v1/dashboard/summary/`
- **Method**: `GET`
- **Description**: Retrieve consolidated data for the dashboard.
- **Response**:
  ```json
  {
    "total_stock_value": "15000.00",
    "low_stock_items": [
      {
        "name": "Hydrochloric Acid",
        "sku": "HCL-001",
        "current_stock": "50.00",
        "min_stock": "100.00"
      }
    ],
    "expiring_soon_items": [
      {
        "reagent": "Sodium Chloride",
        "lot_number": "NACL20250917",
        "expiry_date": "2025-10-15",
        "quantity": "1000.00"
      }
    ],
    "consumption_data": {
      "labels": ["2025-07", "2025-08", "2025-09"],
      "values": [1500.0, 1800.0, 2100.0]
    },
    "expiry_data": {
      "labels": ["Expired", "Expiring in 90 days", "Valid"],
      "values": [2, 5, 15]
    }
  }
  ```

### Reports

#### Financial Report
- **URL**: `/api/v1/reports/financial/`
- **Method**: `GET`
- **Description**: Generate a financial report.
- **Query Parameters**:
  - `start_date` (required): Start date in YYYY-MM-DD format
  - `end_date` (required): End date in YYYY-MM-DD format
- **Response**:
  ```json
  {
    "total_spent": "2500.00",
    "period": "2025-01-01 to 2025-03-31"
  }
  ```

#### Consumption by User Report
- **URL**: `/api/v1/reports/consumption-by-user/`
- **Method**: `GET`
- **Description**: Generate a report on reagent consumption by user.
- **Query Parameters**:
  - `start_date` (required): Start date in YYYY-MM-DD format
  - `end_date` (required): End date in YYYY-MM-DD format
- **Response**:
  ```json
  [
    {
      "user__username": "analyst1",
      "stock_lot__reagent__name": "Sodium Chloride",
      "total_quantity": "150.00"
    }
  ]
  ```

#### Waste/Loss Report
- **URL**: `/api/v1/reports/waste-loss/`
- **Method**: `GET`
- **Description**: Generate a report on reagent waste and loss.
- **Query Parameters**:
  - `start_date` (required): Start date in YYYY-MM-DD format
  - `end_date` (required): End date in YYYY-MM-DD format
- **Response**:
  ```json
  [
    {
      "stock_lot__reagent__name": "Hydrochloric Acid",
      "move_type": "Descarte",
      "total_quantity": "50.00"
    }
  ]
  ```

#### Stock Value Report
- **URL**: `/api/v1/reports/stock-value/`
- **Method**: `GET`
- **Description**: Calculate the total value of all stock lots.
- **Query Parameters**:
  - `group_by` (optional): Group by 'category' or 'location'
- **Response**:
  ```json
  {
    "total_value": "15000.00"
  }
  ```

#### Expiry Report
- **URL**: `/api/v1/reports/expiry/`
- **Method**: `GET`
- **Description**: Generate a report of reagents with upcoming or past expiry dates.
- **Query Parameters**:
  - `days_until_expiry` (optional): Number of days until expiry
  - `expired` (optional): Boolean to show only expired items
- **Response**:
  ```json
  [
    {
      "reagent__name": "Sodium Chloride",
      "lot_number": "NACL20250917",
      "expiry_date": "2025-10-15",
      "current_quantity": "1000.00",
      "location__name": "Shelf A-3"
    }
  ]
  ```

### Requisitions

#### List Requisitions
- **URL**: `/api/v1/requisitions/`
- **Method**: `GET`
- **Description**: Retrieve a list of all requisitions.
- **Response**:
  ```json
  [
    {
      "id": 1,
      "requester": 2,
      "reagent": 1,
      "quantity": "100.00",
      "status": "Pendente",
      "approver": null,
      "request_date": "2025-09-17T09:00:00Z",
      "approval_date": null
    }
  ]
  ```

#### Create Requisition
- **URL**: `/api/v1/requisitions/`
- **Method**: `POST`
- **Description**: Create a new requisition.
- **Request Body**:
  ```json
  {
    "requester": 2,
    "reagent": 1,
    "quantity": "100.00"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "requester": 2,
    "reagent": 1,
    "quantity": "100.00",
    "status": "Pendente",
    "approver": null,
    "request_date": "2025-09-17T09:00:00Z",
    "approval_date": null
  }
  ```

#### Approve Requisition
- **URL**: `/api/v1/requisitions/{id}/approve/`
- **Method**: `POST`
- **Description**: Approve a requisition.
- **Response**:
  ```json
  {
    "status": "requisition approved"
  }
  ```

#### Reject Requisition
- **URL**: `/api/v1/requisitions/{id}/reject/`
- **Method**: `POST`
- **Description**: Reject a requisition.
- **Response**:
  ```json
  {
    "status": "requisition rejected"
  }
  ```