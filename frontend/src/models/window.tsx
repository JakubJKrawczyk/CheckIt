type WindowSize = [number, number];

type WindowConfig = { [key: string]: never };

type WindowStorage = { [key: string]: never };

export interface WindowModel {
    title?: string;
    id?: string;
    parent?: WindowModel;
    size: WindowSize;
    config?: WindowConfig;
    url?: string;
    storage: WindowStorage;
}

export class WindowModelClass implements WindowModel {
    title?: string;
    id?: string;
    parent?: WindowModel;
    size: WindowSize;
    config?: WindowConfig;
    url?: string;
    storage: WindowStorage;

    constructor(
        title: string | undefined = undefined,
        id: string | undefined = undefined,
        parent: WindowModel | undefined = undefined,
        size: WindowSize = [0, 0],
        config: WindowConfig | undefined = undefined,
        url: string | undefined = undefined
    ) {
        this.title = title;
        this.id = id;
        this.parent = parent;
        this.size = size;
        this.config = config;
        this.url = url;
        this.storage = {};
    }
}