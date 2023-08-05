"""Test cases for testing ElasticTabstops."""

import unittest
from elastictabstops import to_elastic_tabstops, to_spaces, MULTIPLE_TOKEN, _cell_exists, _replace_multiple_spaces


ET_TEXT_1 = r"""
abc

	def
	ghi

		jkl
		mno

			pqr
			stu

vwx
"""

SPACE_TEXT_1 = r"""
abc

        def
        ghi

                jkl
                mno

                        pqr
                        stu

vwx
"""


ET_TEXT_2 = r"""aaa

	abc
	def
		ghi
		jkl

	mno
	pqr

		stu
		vwx
"""

SPACE_TEXT_2 = r"""aaa

        abc
        def
                ghi
                jkl

        mno
        pqr

                stu
                vwx
"""


ET_TEXT_3 = r"""
	abc
	def

	ghi
x	jkl

	mno
xxxxxxxxx	pqr
"""

SPACE_TEXT_3 = r"""
        abc
        def

        ghi
x       jkl

                mno
xxxxxxxxx       pqr
"""


ET_TEXT_4 = r"""
	abc
	def	ghi
	jkl	mno
	pqr
"""

SPACE_TEXT_4 = r"""
        abc
        def     ghi
        jkl     mno
        pqr
"""


ET_FORMATTED_CODE = r"""
/* Hopefully this Java program should demonstrate how elastic tabstops work.	*/
/* Try inserting and deleting different parts of the text and watch as the tabstops move.	*/
/* If you like this, please ask the writers of your text editor to implement it.	*/

#include <stdio.h>

struct ipc_perm
{
	key_t	key;
	ushort	uid;	/* owner euid and egid	*/
	ushort	gid;	/* group id	*/
	ushort	cuid;	/* creator euid and egid	*/
	cell-missing		/* for test purposes	*/
	ushort	mode;	/* access modes	*/
	ushort	seq;	/* sequence number	*/
};

int someDemoCode(	int fred,
	int wilma)
{
	x();	/* try making	*/
	printf("hello!\n");	/* this comment	*/
	doSomethingComplicated();	/* a bit longer	*/
	for (i = start; i < end; ++i)
	{
		if (isPrime(i))
		{
			++numPrimes;
		}
	}
	return numPrimes;
}

---- and now for something completely different: a table ----

Title	Author	Publisher	Year
Generation X	Douglas Coupland	Abacus	1995
Informagic	Jean-Pierre Petit	John Murray Ltd	1982
The Cyberiad	Stanislaw Lem	Harcourt Publishers Ltd	1985
The Selfish Gene	Richard Dawkins	Oxford University Press	2006
"""

SPACE_FORMATTED_CODE_MIN_2 = r"""
/* Hopefully this Java program should demonstrate how elastic tabstops work.               */
/* Try inserting and deleting different parts of the text and watch as the tabstops move.  */
/* If you like this, please ask the writers of your text editor to implement it.           */

#include <stdio.h>

struct ipc_perm
{
    key_t         key;
    ushort        uid;   /* owner euid and egid    */
    ushort        gid;   /* group id               */
    ushort        cuid;  /* creator euid and egid  */
    cell-missing         /* for test purposes      */
    ushort        mode;  /* access modes           */
    ushort        seq;   /* sequence number        */
};

int someDemoCode(  int fred,
                   int wilma)
{
    x();                       /* try making    */
    printf("hello!\n");        /* this comment  */
    doSomethingComplicated();  /* a bit longer  */
    for (i = start; i < end; ++i)
    {
        if (isPrime(i))
        {
            ++numPrimes;
        }
    }
    return numPrimes;
}

---- and now for something completely different: a table ----

Title             Author             Publisher                Year
Generation X      Douglas Coupland   Abacus                   1995
Informagic        Jean-Pierre Petit  John Murray Ltd          1982
The Cyberiad      Stanislaw Lem      Harcourt Publishers Ltd  1985
The Selfish Gene  Richard Dawkins    Oxford University Press  2006
"""

SPACE_FORMATTED_CODE_MOD_8 = r"""
/* Hopefully this Java program should demonstrate how elastic tabstops work.                    */
/* Try inserting and deleting different parts of the text and watch as the tabstops move.       */
/* If you like this, please ask the writers of your text editor to implement it.                */

#include <stdio.h>

struct ipc_perm
{
        key_t           key;
        ushort          uid;    /* owner euid and egid          */
        ushort          gid;    /* group id                     */
        ushort          cuid;   /* creator euid and egid        */
        cell-missing            /* for test purposes            */
        ushort          mode;   /* access modes                 */
        ushort          seq;    /* sequence number              */
};

int someDemoCode(       int fred,
                        int wilma)
{
        x();                            /* try making           */
        printf("hello!\n");             /* this comment         */
        doSomethingComplicated();       /* a bit longer         */
        for (i = start; i < end; ++i)
        {
                if (isPrime(i))
                {
                        ++numPrimes;
                }
        }
        return numPrimes;
}

---- and now for something completely different: a table ----

Title                   Author                  Publisher                       Year
Generation X            Douglas Coupland        Abacus                          1995
Informagic              Jean-Pierre Petit       John Murray Ltd                 1982
The Cyberiad            Stanislaw Lem           Harcourt Publishers Ltd         1985
The Selfish Gene        Richard Dawkins         Oxford University Press         2006
"""


#def show_diffs(string1, string2):
#	import difflib
#	print(''.join(difflib.unified_diff(string1, string2)))


def show_diffs(string1, string2):
	"""
	Unify operations between two compared strings
	see: http://stackoverflow.com/questions/774316/python-difflib-highlighting-differences-inline
	"""
	import difflib
	seqm = difflib.SequenceMatcher(None, string1, string2)
	changed = False
	output = []
	for opcode, a_0, a_1, b_0, b_1 in seqm.get_opcodes():
		if opcode == 'equal':
			output.append(seqm.a[a_0:a_1])
		elif opcode == 'insert':
			output.append("<ins>" + seqm.b[b_0:b_1] + "</ins>")
			changed = True
		elif opcode == 'delete':
			output.append("<del>" + seqm.a[a_0:a_1] + "</del>")
			changed = True
		elif opcode == 'replace':
			#raise NotImplementedError, "what to do with 'replace' opcode?"
			output.append("<rep>" + seqm.a[a_0:a_1] + "<became>" + seqm.a[b_0:b_1] + "</rep>")
			changed = True
		else:
			raise RuntimeError, "unexpected opcode"
	if changed:
		print ''.join(output)


def show_debug_info(string1, string2):
	"""Show differences and other debug info about 2 strings."""
	show_diffs(string1, string2)
	if string1 != string2:
		print 'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv string 1 vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'
		print string1
		print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ string 1 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
		print 'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv string 2 vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'
		print string2
		print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ string 2 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'


TEST_STRINGS_LIST = [
	{'et_text': ET_FORMATTED_CODE, 'space_text': SPACE_FORMATTED_CODE_MOD_8},
	{'et_text': ET_TEXT_1, 'space_text': SPACE_TEXT_1},
	{'et_text': ET_TEXT_2, 'space_text': SPACE_TEXT_2},
	{'et_text': ET_TEXT_3, 'space_text': SPACE_TEXT_3},
	{'et_text': ET_TEXT_4, 'space_text': SPACE_TEXT_4},
]


class TestElasticTabstops(unittest.TestCase):
	"""Test case for testing ElasticTabstops."""

	def test_to_elastic_tabstops(self):
		"""Test to_elastic_tabstops()."""
		for test_strings in TEST_STRINGS_LIST:
			string1 = test_strings['et_text']
			string2 = to_elastic_tabstops(test_strings['space_text'], tab_size=8)
			self.assertEqual(string1, string2, show_debug_info(string1, string2))

	def test_to_spaces(self):
		"""Test to_spaces()."""
		for test_strings in TEST_STRINGS_LIST:
			string1 = test_strings['space_text']
			string2 = to_spaces(test_strings['et_text'], tab_size=8)
			self.assertEqual(string1, string2, show_debug_info(string1, string2))

	def test_cell_exists(self):
		"""Test _cell_exists()."""
		list_of_lists = [[], [1], [2, 3], [4, 5, 6], ]
		self.assertFalse(_cell_exists(list_of_lists, 0, 0))
		self.assertFalse(_cell_exists(list_of_lists, 1, 1))
		self.assertFalse(_cell_exists(list_of_lists, 2, 2))
		self.assertFalse(_cell_exists(list_of_lists, 3, 3))
		self.assertFalse(_cell_exists(list_of_lists, 4, 0))
		self.assertTrue(_cell_exists(list_of_lists, 1, 0))
		self.assertTrue(_cell_exists(list_of_lists, 2, 1))
		self.assertTrue(_cell_exists(list_of_lists, 3, 2))

	def test_replace_multiple_spaces(self):
		"""Test _replace_multiple_spaces()."""
		self.assertEqual(_replace_multiple_spaces(' x x x '), ' x x x ')
		self.assertEqual(_replace_multiple_spaces('  x x x '), '%c%cx x x ' % ((MULTIPLE_TOKEN,) * 2))
		self.assertEqual(_replace_multiple_spaces(' x x x  '), ' x x x%c%c' % ((MULTIPLE_TOKEN,) * 2))
		self.assertEqual(_replace_multiple_spaces('  x x x  '), '%c%cx x x%c%c' % ((MULTIPLE_TOKEN,) * 4))
		self.assertEqual(_replace_multiple_spaces(' x  x x '), ' x%c%cx x ' % ((MULTIPLE_TOKEN,) * 2))
		self.assertEqual(_replace_multiple_spaces(' x x  x '), ' x x%c%cx ' % ((MULTIPLE_TOKEN,) * 2))
		self.assertEqual(_replace_multiple_spaces('  x  x x '), '%c%cx%c%cx x ' % ((MULTIPLE_TOKEN,) * 4))
		self.assertEqual(_replace_multiple_spaces('  x  x  x '), '%c%cx%c%cx%c%cx ' % ((MULTIPLE_TOKEN,) * 6))
		self.assertEqual(_replace_multiple_spaces('  x  x  x  '), '%c%cx%c%cx%c%cx%c%c' % ((MULTIPLE_TOKEN,) * 8))
		self.assertEqual(_replace_multiple_spaces('   xx   xx   xx   '), '%c%c%cxx%c%c%cxx%c%c%cxx%c%c%c' % ((MULTIPLE_TOKEN,) * 12))


if __name__ == '__main__':
	unittest.main()
