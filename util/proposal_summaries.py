import os
import zipfile

from data.proposal import summary_file


def zip_proposal_summaries(proposal_codes, semester, file):
    """
    Zip the summary files of a list of proposals into a single zip file.

    Parameters
    ----------
    proposal_codes : iterable of str
        Proposal codes such as "2018-1-SCI-008".
    semester : str
        The semester, such as '2018-1'.
    file : str or file-like or path-like
        File into which the zip content is written. If a file-like object is passed, its mode must be 'wb'.
    """

    with zipfile.ZipFile(file, mode='w') as summary_zip:
        for proposal_code in proposal_codes:
            summary = summary_file(proposal_code, semester)
            if not os.path.exists(summary):
                raise Exception('Summary file not found: {summary}'.format(summary=summary))
            summary_zip.write(str(summary), str(os.path.join('{proposal_code}.pdf'.format(proposal_code=proposal_code))))
