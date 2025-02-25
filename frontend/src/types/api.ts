export interface PaginatedResult<T> {
  total: number,
  skip: number,
  limit: number,
  records: T[],
  _started: boolean
}


export function defaultResult<T>() {
  const r: PaginatedResult<T> = {
    total: 0,
    skip: 0,
    limit: 0,
    records: [],
    _started: false
  }

  return r;
}
