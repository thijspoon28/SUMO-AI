import { type Basho } from "./basho";
import { type Rikishi } from "./rikishi";

export interface RikishiBasho {
    rikishiId: number;
    bashoId: string;
    specialPrize: string;
    yusho?: string;
    rikishi?: Rikishi;
    basho?: Basho;
}
