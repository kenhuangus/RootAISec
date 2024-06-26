const fs = require("fs");

async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Using account:", deployer.address);

  const contractAddress = fs.readFileSync("contract.txt").toString().trim();

  const RootAISecToken = await ethers.getContractFactory("RootAISecToken");
  const rootAISecToken = RootAISecToken.attach(contractAddress);

  // Call the listAdmins function on the contract
  const admins = await rootAISecToken.rewardTokens(
    "0x99b31DD09146955ed2F93Cd8199185Fd3cEED292",
    100000
  );

  // Log the list of admins
  console.log("Admins:", admins);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
