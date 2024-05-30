async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);

  const initialSupply = ethers.utils.parseUnits('1000000000', 18); // 1 billion tokens

  const RootAISecToken = await ethers.getContractFactory("RootAISecToken");
  const rootAISecToken = await RootAISecToken.deploy(initialSupply);

  await rootAISecToken.deployed();

  console.log("RootAISecToken deployed to:", rootAISecToken.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
