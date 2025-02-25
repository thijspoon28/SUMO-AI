import type { Match } from "./match";

export interface Basho {
    id: string,
    date: string,
    start_date: Date,
    end_date: Date,
    matches: Match[]
}
