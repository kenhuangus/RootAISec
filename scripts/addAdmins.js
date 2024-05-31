const fs = require("fs");

async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Using account:", deployer.address);

  const contractAddress = fs.readFileSync("contract.txt").toString().trim();

  const RootAISecToken = await ethers.getContractFactory("RootAISecToken");
  const rootAISecToken = RootAISecToken.attach(contractAddress);

  const ken = ethers.utils.getAddress(
    "0x88250F772101179a4EcfAA4b92a983676a3cE445"
  ); // Replace with the new admin's address
  await rootAISecToken.connect(deployer).addAdmin(ken);

  console.log("Added new admin:", ken);

  // Add a new admin
  const lane = "0xF1Fff00f308055dE173a0cD390C36f9A44fEB2de"; // Replace with the new admin's address
  await rootAISecToken.connect(deployer).addAdmin(lane);

  console.log("Added new admin:", lane);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
