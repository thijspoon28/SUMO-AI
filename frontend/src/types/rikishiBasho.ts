import { Basho } from "./basho";
import { Rikishi } from "./rikishi";

export interface RikishiBasho {
    rikishiId: number;
    bashoId: string;
    specialPrize: string;
    yusho?: string;
    rikishi?: Rikishi;
    basho?: Basho;
}
