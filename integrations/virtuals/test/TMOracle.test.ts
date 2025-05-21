import { expect } from "chai";
import { ethers } from "hardhat";
import { Contract, ContractFactory } from "ethers";
import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/signers";

describe("TMOracle", function () {
  let TMOracle: ContractFactory;
  let MockVeTMAI: ContractFactory;
  let oracle: Contract;
  let veTMAI: Contract;
  let owner: SignerWithAddress;
  let keeper: SignerWithAddress;
  let user: SignerWithAddress;
  let noStakeUser: SignerWithAddress;

  beforeEach(async function () {
    // Deploy mock veTMAI token
    const MockVeTMAI = await ethers.getContractFactory("MockVeTMAI");
    [owner, keeper, user, noStakeUser] = await ethers.getSigners();
    veTMAI = await MockVeTMAI.deploy();
    await veTMAI.deployed();

    // Set up stake for testing
    await veTMAI.setBalance(user.address, ethers.utils.parseEther("10"));
    
    // Deploy TMOracle
    TMOracle = await ethers.getContractFactory("TMOracle");
    oracle = await TMOracle.deploy(veTMAI.address);
    await oracle.deployed();
    
    // Set keeper
    await oracle.setKeeper(keeper.address);
  });

  it("Should set the right owner and keeper", async function () {
    expect(await oracle.owner()).to.equal(owner.address);
    expect(await oracle.keeper()).to.equal(keeper.address);
  });

  it("Should update ratings correctly", async function () {
    const symbol = "BTC";
    const rating = 8570; // 85.7
    const technical = 8230; // 82.3
    const fundamental = 8810; // 88.1
    
    await oracle.connect(keeper).updateRating(symbol, rating, technical, fundamental);
    
    const storedRating = await oracle.ratings(symbol);
    expect(storedRating.symbol).to.equal(symbol);
    expect(storedRating.rating).to.equal(rating);
    expect(storedRating.technical).to.equal(technical);
    expect(storedRating.fundamental).to.equal(fundamental);
    
    const symbols = await oracle.getAllSymbols();
    expect(symbols).to.include(symbol);
  });

  it("Should allow users with stake to get ratings", async function () {
    const symbol = "ETH";
    const rating = 9020; // 90.2
    const technical = 8950; // 89.5
    const fundamental = 9150; // 91.5
    
    await oracle.connect(keeper).updateRating(symbol, rating, technical, fundamental);
    
    const storedRating = await oracle.connect(user).getRating(symbol);
    expect(storedRating.symbol).to.equal(symbol);
    expect(storedRating.rating).to.equal(rating);
  });

  it("Should revert if caller has no veTMAI stake", async function () {
    const symbol = "SOL";
    const rating = 7560; // 75.6
    const technical = 7230; // 72.3
    const fundamental = 7710; // 77.1
    
    await oracle.connect(keeper).updateRating(symbol, rating, technical, fundamental);
    
    await expect(
      oracle.connect(noStakeUser).getRating(symbol)
    ).to.be.revertedWith("TMOracle: caller has no veTMAI stake");
  });

  it("Should revert if rating not found", async function () {
    await expect(
      oracle.connect(user).getRating("NONEXISTENT")
    ).to.be.revertedWith("TMOracle: rating not found");
  });
});
