import type { Match } from "./match";

export interface Basho {
    id: string,
    date: string,
    start_date: string,
    end_date: string,
    matches: Match[]
}
