type WindowSize = [number, number];

type WindowConfig = { [key: string]: never };

type WindowStorage = { [key: string]: never };

export interface WindowModel {
    title?: string;
    window_id?: string;
    parent?: WindowModel;
    size: WindowSize;
    config?: WindowConfig;
    url?: string;
    storage: WindowStorage;
}

export class WindowModelClass implements WindowModel {
    public title?: string;
    public window_id?: string;
    public parent?: WindowModel;
    public size: WindowSize;
    public config?: WindowConfig;
    public url?: string;
    public storage: WindowStorage;

    constructor(
        title: string | undefined = undefined,
        window_id: string | undefined = undefined,
        parent: WindowModel | undefined = undefined,
        size: WindowSize = [0, 0],
        config: WindowConfig | undefined = undefined,
        url: string | undefined = undefined
    ) {
        this.title = title;
        this.window_id = window_id;
        this.parent = parent;
        this.size = size;
        this.config = config;
        this.url = url;
        this.storage = {};
    }
}


