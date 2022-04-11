# Enron emails clustering

# Description

This project aims at clustering the emails related to the [ENRON scandal](https://en.wikipedia.org/wiki/Enron_scandal). The email data set comes form https://www.cs.cmu.edu/~enron/.

# The team

- [Tony Anciaux](https://github.com/TonyAnciaux)
- [Biniam Behre](https://github.com/BiniamBerhe)
- [Giovanna Fauro](https://github.com/Gio-F)
- [Quentin Lambotte](https://github.com/qlambotte)

# Roadmap

MVP: streamlit interface that shows the tree of categories; at a leaf of the tree shows the list of emails that are clickable.

We broke the task in two main steps.
1. clusturing engine
   - quick research of libraries for clustering, specialised in NLP
   - explore the data:
     * how do we represent the data? Vectorization?
     * cleaning
   - labeling
     * read about automated labelling of clusters
   - choose algo for clusturing
2. the interface (streamlit)
   - introduction text
   - the tree implementation
   - the leafs implementation (the path to the leaf, list of emails, and how to read them)

Our first goal is to have a _functionning_ clusturing engine by **Wednesday 13/04**.


1. Monday 11/04

- Todo list:

  - [x] create repo  
  - [x] update the readme  
  - [ ] read as much on the available tools  
  - [ ] decide which tools to use.  
  - [ ] look a little in the dataset to see how messy it is  
  - [ ] Quick catch-up meeting after techtalk.  
  - [ ] Implement usage of Trello  

- Who does what:
  1. Q: create repo and readme
  2. Q: look at the data
  3. B: clustering (in general + libraries available)
  4. T: automated labelling
  5. G: how to encode the text parts of the data.
  6. G: implement usage of Trello

# Bonus features

1. deploy using docker and host the webapp online
