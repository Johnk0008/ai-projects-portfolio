# 🗳️ Polling System Smart Contract

## Complete Implementation
A complete blockchain-based polling system that demonstrates smart contract functionality for creating polls, voting, and determining winners.

## 📋 Features Implemented

✅ **Poll Structure** - Title, options, end time, vote count mappings  
✅ **Poll Creation** - Users can create polls with options and deadlines  
✅ **Single Vote Restriction** - Each address can vote only once  
✅ **Time-Based Restrictions** - Voting only allowed before deadline  
✅ **Secure Storage** - Mappings prevent double voting  
✅ **Winner Determination** - Function returns winning option after poll ends  

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- VS Code (recommended)

### Installation & Execution

1. **Setup Virtual Environment**:
   ```bash
   python -m venv polling_env
   source polling_env/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install web3==6.0.0 eth-tester==0.9.0 python-dotenv==1.0.0
   ```

3. **Run the System**:
   ```bash
   python verify_solidity.py    # Verify contract structure
   python working_polling_system.py  # Run main demonstration
   ```

## 🎯 Execution Order

1. **Start**: `python verify_solidity.py`
2. **Main Demo**: `python working_polling_system.py`
3. **Dependency Check**: `python check_simple_deps.py` (if needed)

## 🔧 Files Description

- **`working_polling_system.py`** - Main simulator demonstrating all features
- **`PollingContract.sol`** - Solidity smart contract implementation
- **`verify_solidity.py`** - Validates contract structure without compilation
- **`check_simple_deps.py`** - Checks and installs required packages
- **`compile_simple.py`** - Optional compilation script

## 🎉 Expected Output

When running `working_polling_system.py`, you'll see:
- Poll creation with multiple options
- Simulated voting process
- Real-time vote counting
- Double voting prevention
- Time-based restrictions
- Winner determination
- Feature demonstration summary

## 📊 Demo Statistics

- Multiple polls creation
- 6+ simulated voters
- Real-time results display
- Security feature testing
- Comprehensive feature validation

## 🛠️ Technology Stack

- **Blockchain**: Ethereum Smart Contracts (Solidity)
- **Simulation**: Python Web3 & Custom Simulator
- **Environment**: Python 3.9 Virtual Environment
- **IDE**: VS Code with Solidity support

---