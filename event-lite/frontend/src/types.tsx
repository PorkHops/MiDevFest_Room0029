// src/types.ts
export interface Event {
  id: string | number;
  title: string;
  venue: string;
  date: string;
  price: string;
  image: string;
  url: string;
  summary: string;
}

export type Location = { lat: number; lng: number } | null;
