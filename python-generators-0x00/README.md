# Python Generators Project - ALX Backend Specialization

## 📚 Overview

This project demonstrates the power and versatility of Python generators in handling large datasets and interacting with databases efficiently. It is designed as part of the ALX Backend curriculum to simulate real-world data processing scenarios, memory-optimized operations, and integration with SQL databases.

---

## 🚀 Learning Objectives

By completing this project, you will be able to:

- ✅ Understand and implement Python generators using `yield`
- ✅ Handle and process large datasets from a MySQL database
- ✅ Use generators for streaming, batching, pagination, and aggregation
- ✅ Apply lazy loading techniques
- ✅ Integrate Python with SQL using connectors and dynamic queries
- ✅ Optimize performance by reducing memory usage

---

## 🛠️ Technologies Used

- **Python 3.x**
- **MySQL** (for database operations)
- **MySQL Connector for Python**
- **CSV for data seeding**
- **Git** for version control

---

## 📁 Project Structure

```plaintext
python-generators-0x00/
├── seed.py                   # Seeds the MySQL DB and populates user_data
├── user_data.csv             # Contains sample user data
├── 0_stream_user.py          # Streams users row-by-row from DB
├── 0-main.py                 # Test for Task 0
├── 1-batch_processing.py     # Processes users in batches (age > 25)
├── 1-main.py                 # Test for Task 1
├── 2-lazy_paginate.py        # Implements lazy pagination
├── 2-main.py                 # Test for Task 2
├── 3-main.py                 # Alternative test for lazy pagination
├── 4-stream_ages.py          # Memory-efficient average age calculation
├── 4-main.py                 # Test for average age generator
