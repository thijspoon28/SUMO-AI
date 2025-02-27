import type { Match } from "./match";
import type { RikishiBasho } from "./rikishiBasho";

export interface Basho {
    id: string;
    date: string;
    startDate: string;
    endDate: string;
    rikishi?: RikishiBasho[];
    matches?: Match[];
}
