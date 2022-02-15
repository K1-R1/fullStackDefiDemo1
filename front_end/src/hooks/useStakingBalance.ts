import { useContractCall, useEthers } from "@usedapp/core"
import TokenFarm from "../brownie-build/TokenFarm.json"
import { utils, BigNumber, constants } from "ethers"
import networkMapping from "../brownie-build/map.json"

export const useStakingBalance = (address: string): BigNumber | undefined => {
  const { account, chainId } = useEthers()

  const { abi } = TokenFarm
  const tokenFarmContractAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero

  const tokenFarmInterface = new utils.Interface(abi)

  const [stakingBalance] =
    useContractCall({
      abi: tokenFarmInterface,
      address: tokenFarmContractAddress,
      method: "stakingBalance",
      args: [address, account],
    }) ?? []

  return stakingBalance
}
