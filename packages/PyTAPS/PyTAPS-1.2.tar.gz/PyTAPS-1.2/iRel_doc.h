#ifndef PYTAPS_IREL_DOC_H
#define PYTAPS_IREL_DOC_H

/***** iRel.Rel *****/

#define IRELDOC_iRel \
"Return a new :class:`Rel` object with any implementation-specific\n"          \
"options defined in *options*.\n\n"                                            \
":param options: Implementation-specific options string"

#define IRELDOC_iRel_createPair \
"Create a new relation pair between two ITAPS interfaces.\n\n"                 \
":param first: The interface on the left half of the pair\n"                   \
":param first_type: The relation :class:`Type` for the first\n"                \
"                   interface\n"                                               \
":param second: The interface on the right half of the pair\n"                 \
":param second_type: The relation :class:`Type` for the second\n"              \
"                    interface\n"                                              \
":return: The newly-created relation pair"

#define IRELDOC_iRel_destroyPair \
"Destroy a relation pair.\n\n"                                                 \
":param pair: The relation pair to be destroyed"

#define IRELDOC_iRel_findPairs \
"Find all relation pairs that contain the specified *interface*.\n\n"          \
":param interface: The interface to search for\n"                              \
":return: A list of relation pairs"

/***** iRel.Pair *****/

#define IRELDOC_iRelPair \
"Return a new set referring to the handled contained in *set*. If *set* is\n"  \
"an :class:`itaps.iBase.EntitySet` instance, *instance* must also be\n"        \
"specified."

#define IRELDOC_iRelPair_instance \
"Return the :class:`Rel` instance from which this pair was created."

#define IRELDOC_iRelPair_first \
"Return the instance corresponding to the left half of this relation\n"        \
"pair."

#define IRELDOC_iRelPair_second \
"Return the instance corresponding to the right half of this relation\n"       \
"pair."

#define IRELDOC_iRelPair_firstType \
"Return the relation :class:`Type` of the left half of this relation\n"        \
"pair."

#define IRELDOC_iRelPair_secondType \
"Return the relation :class:`Type` of the right half of this relation\n"       \
"pair."

#define IRELDOC_iRelPair_setRelation \
"Relate two elements (entities or sets) to one another. If *first*\n"          \
"and *second* are arrays, relate the elements pairwise.\n\n"                   \
":param first: :class:`~itaps.iBase.Entity` or\n"                              \
"              :class:`~itaps.iBase.EntitySet` from the left half of\n"        \
"              the relation pair\n"                                            \
":param second: :class:`~itaps.iBase.Entity` or\n"                             \
"               :class:`~itaps.iBase.EntitySet` from the right half\n"         \
"               of the relation pair"

#define IRELDOC_iRelPair_getEntRelation \
"Get the entity related to the specified element. One of *first* or\n"         \
"*second* must be defined (as a keyword argument). Alternately, you\n"         \
"may supply an entity and a boolean flag *swapped* where *False*\n"            \
"specifies that you have an element from the left half and *True*\n"           \
"specifies that you have an entity from the right half. If the input\n"        \
"is an array of elements, this function returns pairwise relations.\n\n"       \
":param first: :class:`~itaps.iBase.Entity` or\n"                              \
"              :class:`~itaps.iBase.EntitySet` from the left half of\n"        \
"              the relation pair\n"                                            \
":param second: :class:`~itaps.iBase.Entity` or\n"                             \
"               :class:`~itaps.iBase.EntitySet` from the right half\n"         \
"               of the relation pair\n"                                        \
":return: The related entity"

#define IRELDOC_iRelPair_getEntArrRelation \
"Get the entities related to the specified element. One of *first*\n"          \
"or *second* must be defined (as a keyword argument). Alternately,\n "         \
"you may supply an entity and a boolean flag *swapped* where\n"                \
"*False* specifies that you have an element from the left half and\n"          \
"*True* specifies that you have an entity from the right half. If\n"           \
"the input is an array of elements, this function returns pairwise\n"          \
"relations.\n\n"                                                               \
":param first: :class:`~itaps.iBase.Entity` or\n"                              \
"              :class:`~itaps.iBase.EntitySet` from the left half of\n"        \
"              the relation pair\n"                                            \
":param second: :class:`~itaps.iBase.Entity` or\n"                             \
"               :class:`~itaps.iBase.EntitySet` from the right half\n"         \
"               of the relation pair\n"                                        \
":return: The related entities"

#define IRELDOC_iRelPair_getSetRelation \
"Get the set related to the specified element. One of *first* or\n"            \
"*second* must be defined (as a keyword argument). Alternately, you\n"         \
"may supply an entity and a boolean flag *swapped* where *False*\n"            \
"specifies that you have an element from the left half and *True*\n"           \
"specifies that you have an entity from the right half. If the input\n"        \
"is an array of elements, this function returns pairwise relations.\n\n"       \
":param first: :class:`~itaps.iBase.Entity` or\n"                              \
"              :class:`~itaps.iBase.EntitySet` from the left half of\n"        \
"              the relation pair\n"                                            \
":param second: :class:`~itaps.iBase.Entity` or\n"                             \
"               :class:`~itaps.iBase.EntitySet` from the right half\n"         \
"               of the relation pair\n"                                        \
":return: The related entity set"

#define IRELDOC_iRelPair_getSetArrRelation  \
"Get the sets related to the specified element. One of *first* or\n"           \
"*second* must be defined (as a keyword argument). Alternately, you\n"         \
"may supply an entity and a boolean flag *swapped* where *False*\n"            \
"specifies that you have an element from the left half and *True*\n"           \
"specifies that you have an entity from the right half. If the input\n"        \
"is an array of elements, this function returns pairwise relations.\n\n"       \
":param first: :class:`~itaps.iBase.Entity` or\n"                              \
"              :class:`~itaps.iBase.EntitySet` from the left half of\n"        \
"              the relation pair\n"                                            \
":param second: :class:`~itaps.iBase.Entity` or\n"                             \
"               :class:`~itaps.iBase.EntitySet` from the right half\n"         \
"               of the relation pair\n"                                        \
":return: The related entity sets"

#define IRELDOC_iRelPair_inferAllRelations \
"Infer the relations between elements (entities or sets) in the\n"             \
"interfaces defined by this relation pair. The criteria used to\n"             \
"infer these relations depends on the interfaces in the pair, the\n"           \
"iRel implementation, and the source of the data in those\n"                   \
"interfaces."

#define IRELDOC_iRelPair_inferRelations \
"Infer the relations corresponding to the supplied element(s)\n"               \
"(entities or sets) in the interfaces defined by this relation pair.\n"        \
"One of *first* or *second* must be defined (as a keyword argument).\n"        \
"Alternately, you may supply an entity and a boolean flag *swapped*\n"         \
"where *False* specifies that you have an element from the left half\n"        \
"and *True* specifies that you have an entity from the right half.\n"          \
"The criteria used to infer these relations depends on the\n"                  \
"interfaces in the pair, the iRel implementation, and the source of\n"         \
"the data in those interfaces.\n\n"                                            \
":param first: :class:`~itaps.iBase.Entity` or\n"                              \
"              :class:`~itaps.iBase.EntitySet` from the left half of\n"        \
"              the relation pair\n"                                            \
":param second: :class:`~itaps.iBase.Entity` or\n"                             \
"               :class:`~itaps.iBase.EntitySet` from the right half\n"         \
"               of the relation pair"

#endif
