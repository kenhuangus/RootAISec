describe('RootAISecToken', function () {
  import('chai')
  .then(chai => {
    // Use chai here
  })
  .catch(error => {
    console.error('Failed to import chai:', error);
  });
  let RootAISecToken;
  let rootAISecToken;
  let deployer, user, researcher;
  const initialSupply = ethers.utils.parseUnits('1000000000', 18); // 1 billion tokens
  const rewardAmount = ethers.utils.parseUnits('100', 18); // 100 tokens

  before(async () => {
    const chai = await import('chai');
    global.expect = chai.expect;
    const ethers = (await import('hardhat')).ethers;
  });

  beforeEach(async function () {
    [deployer, user, researcher] = await ethers.getSigners();
    RootAISecToken = await ethers.getContractFactory('RootAISecToken');
    rootAISecToken = await RootAISecToken.deploy(initialSupply);
    await rootAISecToken.deployed();
  });

  it('should mint the initial supply to the deployer', async function () {
    const deployerBalance = await rootAISecToken.balanceOf(deployer.address);
    expect(deployerBalance).to.equal(initialSupply);
  });

  it('should allow minting of new tokens', async function () {
    const mintAmount = ethers.utils.parseUnits('1000', 18); // 1000 tokens
    await rootAISecToken.mint(user.address, mintAmount);

    const userBalance = await rootAISecToken.balanceOf(user.address);
    expect(userBalance).to.equal(mintAmount);
  });

  it('should allow uploading a guide and emit GuideUploaded event', async function () {
    const guideHash = 'guideHash123';
    await expect(rootAISecToken.connect(researcher).uploadGuide(guideHash))
      .to.emit(rootAISecToken, 'GuideUploaded')
      .withArgs(researcher.address, guideHash);
  });

  it('should reward tokens for valid uploaded guide', async function () {
    // Transfer tokens to the contract to ensure it can reward
    await rootAISecToken.transfer(rootAISecToken.address, rewardAmount);

    const guideHash = 'guideHash123';
    const validateGuideOrPrompt = await rootAISecToken.validateGuideOrPrompt(guideHash);
    expect(validateGuideOrPrompt).to.be.true;

    // Upload guide and check balance after reward
    await rootAISecToken.connect(researcher).uploadGuide(guideHash);

    // In a real scenario, the rewardTokens function would be called by the event listener
    await rootAISecToken.rewardTokens(researcher.address, rewardAmount);

    const researcherBalance = await rootAISecToken.balanceOf(researcher.address);
    expect(researcherBalance).to.equal(rewardAmount);
  });

  it('should allow requesting an audit and emit AuditRequested event', async function () {
    const contractHash = 'contractHash123';
    await expect(rootAISecToken.connect(user).requestAudit(contractHash))
      .to.emit(rootAISecToken, 'AuditRequested')
      .withArgs(user.address, contractHash);
  });
});
