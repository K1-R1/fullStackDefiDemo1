import { useContractFunction, useEthers } from "@usedapp/core"
import TokenFarm from "../brownie-build/TokenFarm.json"
import { utils, constants } from "ethers"
import { Contract } from "@ethersproject/contracts"
import networkMapping from "../brownie-build/map.json"

export const useUnstakeTokens = () => {
  const { chainId } = useEthers()

  const { abi } = TokenFarm
  const tokenFarmContractAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero

  const tokenFarmInterface = new utils.Interface(abi)

  const tokenFarmContract = new Contract(
    tokenFarmContractAddress,
    tokenFarmInterface
  )

  return useContractFunction(tokenFarmContract, "unstakeTokens", {
    transactionName: "Unstake tokens",
  })
}
