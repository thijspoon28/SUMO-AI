import type { Match } from "./match";
import type { RikishiBasho } from "./rikishiBasho";

export interface Basho {
    id: string;
    date: string;
    start_date: string;
    end_date: string;
    rikishi: RikishiBasho[];
    matches: Match[];
}
