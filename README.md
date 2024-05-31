
## RootAISec: Automatic Smart Contract Auditing using Generative AI

Welcome to the Automatic Smart Contract Auditing project! This project leverages generative AI to enable automated auditing of smart contracts. It aims to provide a comprehensive platform for security researchers and web3 project owners to enhance the security of smart contracts through collaborative efforts.
Here is the project description in Canva
https://www.canva.com/design/DAGGigW0Rzc/9AWH5pDUaj4B2pX7HFf1IA/edit
and here is website URL:
https://rootaisec.com/


## Features

1. **Automated Auditing**: Use generative AI to automatically audit smart contracts, providing detailed analysis and security scores.
2. **Security Researcher Contributions**: Security researchers can upload smart contract security checklists, auditing reports, and advanced prompts as PDFs.
3. **Evaluation and Reward**: Uploaded documents are evaluated using a large language model (LLM) and a vector database. If the document is approved, the contributor receives 100 RootAISec tokens (symbol: RAS) as a reward.
4. **Web3 Project Owner Audits**: Web3 project owners can upload their smart contracts for auditing and receive a security score. Initially, this service is free. Once the user base scales to 100 users, each audit will cost 100 RAS tokens.

## Getting Started

### Prerequisites

- Django
- Python (Node Package Manager)
- RootStock blockchain (either testnet or mainnet)
- Hardhat

### Installation

Clone the repository:
    ```bash
    git clone https://github.com/kenhuangus/RootAISec
    cd RootAISec
    ```


### Running the Project
revise .env based on the sample env file 
To run the project, use the following command:
```bash
cd app && docker compose up -d && docker compose logs -f app
```

## Usage

### Uploading Documents

- **For Security Researchers**: Upload your smart contract security checklist, auditing report, or advanced prompts as a PDF. The system will evaluate your submission, and if it meets the criteria, you will receive 100 RAS tokens.
  
- **For Web3 Project Owners**: Upload your smart contract for auditing. You will receive a detailed security score. Initially, this service is free. Once we reach 100 users, each audit will cost 100 RAS tokens.

### Rewards and Tokens

- **RootAISec Tokens (RAS)**: Earn tokens by contributing valuable documents. Tokens can be used to pay for future audits once the project scales.

## Contribution

We welcome contributions from the community. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact us at support@rootaisec.com or support@distributedapps.ai.

Thank you for your interest and contributions to the Automatic Smart Contract Auditing project!
