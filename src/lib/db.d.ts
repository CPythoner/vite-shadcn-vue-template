import * as sqlite3 from 'sqlite3';
export declare function openDb(): Promise<import("sqlite").Database<sqlite3.Database, sqlite3.Statement>>;
export declare function initDb(): Promise<import("sqlite").Database<sqlite3.Database, sqlite3.Statement>>;
export interface Podcast {
    id: number;
    title: string;
    description: string | null;
    cover_url: string | null;
    level: string;
    category: string;
    language: string;
    author: string | null;
    rss_url: string | null;
    website_url: string | null;
    episode_count: number;
    latest_episode_at: string | null;
    created_at: string;
    updated_at: string;
    status: string;
}
export declare function getPodcasts(): Promise<Podcast[]>;
export declare function getPodcast(id: number): Promise<Podcast | undefined>;
export declare function createPodcast(podcast: Omit<Podcast, 'id' | 'created_at' | 'updated_at' | 'episode_count' | 'latest_episode_at'>): Promise<number | undefined>;
