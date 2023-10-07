use crate::config::float;

struct Edge {
    from: usize,
    to: usize,
    weight: float,
}

struct Vertex {
    id: usize,
    edges: Vec<usize>,
}

struct Graph {
    edges: Vec<Edge>,
    vertices: Vec<Vertex>,
}

impl Graph {
    pub fn check(&self){
        
    }
    
}
