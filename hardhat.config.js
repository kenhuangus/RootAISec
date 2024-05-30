const fs = require('fs');

require('@nomiclabs/hardhat-ethers');
require('@nomiclabs/hardhat-waffle');

const TESTNET_GAS_MULT = 1.1;

const mnemonic = fs.readFileSync('.testnet.seed-phrase').toString().trim();
if (!mnemonic || mnemonic.split(' ').length !== 12) {
  console.log('unable to retrieve mnemonic from .secret');
}

// Update gas price Testnet
/* Run this first, to use the result in truffle-config:
  curl https://public-node.testnet.rsk.co/ -X POST -H "Content-Type: application/json" \
    --data '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest",false],"id":1}' \
    > .minimum-gas-price-testnet.json
*/
const gasPriceTestnetRaw = fs
  .readFileSync('.minimum-gas-price-testnet.json')
  .toString()
  .trim();
const minimumGasPriceTestnet = parseInt(
  JSON.parse(gasPriceTestnetRaw).result.minimumGasPrice,
  16,
);
if (
  typeof minimumGasPriceTestnet !== 'number' ||
  Number.isNaN(minimumGasPriceTestnet)
) {
  throw new Error(
    'unable to retrieve network gas price from .gas-price-testnet.json',
  );
}
console.log(`Minimum gas price Testnet: ${minimumGasPriceTestnet}`);

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  solidity: '0.8.20',
  networks: {
    rsktestnet: {
      chainId: 31,
      url: "https://rpc.testnet.rootstock.io/DimJ5HOnwd8Z9H8cEsqJ8tSeyTHtxL-T",
      gasPrice: 60000000, // Math.floor(minimumGasPriceTestnet * TESTNET_GAS_MULT),
      gasMultiplier: TESTNET_GAS_MULT,
      accounts: {
        mnemonic: mnemonic,
        initialIndex: 0,
        path: "m/44'/60'/0'/0",
        count: 10,
      },
    },
  },
};

