import { useEthers } from "@usedapp/core"
import helperConfig from "../helper-config.json"
import networkMapping from "../brownie-build/deployments/map.json"
import { constants } from "ethers"
import brownieConfig from "../brownie-config.json"
import dapp from "./public/dapp.png"
import eth from "./public/eth.png"
import dai from "./public/dai.png"
import { Wallet } from "./Wallet"
import { makeStyles } from "@material-ui/core"

export type Token = {
    image: string
    address: string
    name: string
}

const useStyles = makeStyles((theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4)
    }
}))

export const Main = () => {
    // Show token values from the wallet
    // Get the address of different tokens
    // Get the balance of the users wallet

    const classes = useStyles()
    const { chainId, error } = useEthers()
    const networkName = chainId ? helperConfig[chainId] : "dev"
    let stringChainId = String(chainId)
    const dappTokenAddress = chainId ? networkMapping[stringChainId]["DappToken"][0] : constants.AddressZero
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero // brownie config
    const fauTokenAddress = chainId ? brownieConfig["networks"][networkName]["fau_token"] : constants.AddressZero

    const supportedTokens: Array<Token> = [
        {
            image: dapp,
            address: dappTokenAddress,
            name: "DAPP"
        },
        {
            image: eth,
            address: wethTokenAddress,
            name: "WETH"
        },
        {
            image: dai,
            address: fauTokenAddress,
            name: "DAI"
        }
    ]

    return (<>
        <h2 className={classes.title}>Dapp Token App</h2>
        <Wallet supportedTokens={supportedTokens} />
    </>)
}