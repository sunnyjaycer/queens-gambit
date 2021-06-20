from brownie import accounts, reverts, StreamUnlockableNFTFactory
from brownie.network.state import Chain
import pytest

"""
"""

# Contract addresses for Rinkeby
SUPERFLUID_HOST_ADDRESS = ""
SUPERFLUID_CFA_ADDRESS = ""
SUPERFLUID_IDA_ADDRESS = ""
DAIX_ADDRESS = ""
DAI_ADDRESS = ""
SEVEN_DAYS = 60 * 60 * 24 * 7 + 60    # plus 1 min. on each
THIRTY_DAYS = 60 * 60 * 24 * 30 + 60
STREAM_RATE = 1000 # wei per second
MINTING_FEE = 1e18 # 1 ether


# Canary Test
def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()

"""
Test Suite Outline
- SUNFTs can be minted by an NFT holder
- SUNFTs can be contain multiple NFTs
- SUNFTs can be deposited into by anyone including the holder
- SUNFTs will unlock their NFT after depositing rate for duration
- SUNFTs can be destoryed to recover the deposits
- SUNFTs will return locked NFTs to the creator if destoryed before unlocking
"""
#
def test_mint_snuft(gambit, nft, creator, owner):
    """
    SUNFTs can be minted by an NFT holder
    """
    starting_eth = gambit.balance()

    # Approve 2 NFTs to lock into a SUNFT
    nft.approve(gambit.address, 0, {"from": creator})
    nft.approve(gambit.address, 1, {"from": creator})

    # Mint the SUNFT directly to its owner, append the 2nd NFT after mint
    gambit.mint(nft.address, 0, STREAM_RATE, SEVEN_DAYS, owner, {"from": creator})
    # gambit.append(nft.address, 1, STREAM_RATE, SEVEN_DAYS, {"from": creator})

    # Check properties of the SUNFT created
    assert gambit.ownerOf(1) == owner
    assert gambit.getCreator(1) == creator
    assert gambit.getLastStartedAt(1) == 0
    assert gambit.getCurrentIndex(1) == 0
    assert gambit.getPrincipal(1) == 0
    assert gambit.getProgress(1) == 0
    assert nft.ownerOf(0) == gambit.address
    # TODO: Implement fee
    # assert gambit.balance() - starting_eth == MINTING_FEE

    # Check properties for the NFTs in the SUNFT
    assert gambit.getContractAddress(1, 0) == nft.address
    assert gambit.getTokenId(1, 0) == 0
    assert gambit.getRate(1, 0) == STREAM_RATE
    assert gambit.getDuration(1, 0) == SEVEN_DAYS
    assert gambit.getLock(1, 0) == True
    # assert gambit.getContractAddress(1, 1) == nft.address
    # assert gambit.getTokenId(1, 1) == 1
    # assert gambit.getRate(1, 1) == STREAM_RATE
    # assert gambit.getDuration(1, 1) == SEVEN_DAYS
    # assert gambit.getLock(1, 1) == SEVEN_DAYS