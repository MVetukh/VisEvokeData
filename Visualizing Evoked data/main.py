

import os
import numpy as np
import mne


sample_data_folder = mne.datasets.sample.data_path()
sample_data_evk_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis-ave.fif')
evokeds_list = mne.read_evokeds(sample_data_evk_file, baseline=(None, 0),
                                proj=True, verbose=False)


for e in evokeds_list:
    print(f'Condition: {e.comment}, baseline: {e.baseline}')



conds = ('aud/left', 'aud/right', 'vis/left', 'vis/right')
evks = dict(zip(conds, evokeds_list))



evks['aud/left'].plot(exclude=[])



evks['aud/left'].plot(picks='mag', spatial_colors=True, gfp=True)



times = np.linspace(0.05, 0.13, 5)
evks['aud/left'].plot_topomap(ch_type='mag', times=times, colorbar=True)

# %%

fig = evks['aud/left'].plot_topomap(ch_type='mag', times=0.09, average=0.1)
fig.text(0.5, 0.05, 'average from 40-140 ms', ha='center')



mags = evks['aud/left'].copy().pick_types(meg='mag')
mne.viz.plot_arrowmap(mags.data[:, 175], mags.info, extrapolate='local')



evks['vis/right'].plot_joint()


def custom_func(x):
    return x.max(axis=1)


for combine in ('mean', 'median', 'gfp', custom_func):
    mne.viz.plot_compare_evokeds(evks, picks='eeg', combine=combine)


# sphinx_gallery_thumbnail_number = 13
mne.viz.plot_compare_evokeds(evks, picks='MEG 1811', colors=dict(aud=0, vis=1),
                             linestyles=dict(left='solid', right='dashed'))


temp_list = list()
for idx, _comment in enumerate(('foo', 'foo', '', None, 'bar'), start=1):
    _evk = evokeds_list[0].copy()
    _evk.comment = _comment
    _evk.data *= idx  # so we can tell the traces apart
    temp_list.append(_evk)

mne.viz.plot_compare_evokeds(temp_list, picks='mag')



evks['vis/right'].plot_image(picks='meg')


mne.viz.plot_compare_evokeds(evks, picks='eeg', colors=dict(aud=0, vis=1),
                             linestyles=dict(left='solid', right='dashed'),
                             axes='topo', styles=dict(aud=dict(linewidth=1),
                                                      vis=dict(linewidth=1)))


mne.viz.plot_evoked_topo(evokeds_list)



subjects_dir = os.path.join(sample_data_folder, 'subjects')
sample_data_trans_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                      'sample_audvis_raw-trans.fif')



maps = mne.make_field_map(evks['aud/left'], trans=sample_data_trans_file,
                          subject='sample', subjects_dir=subjects_dir)
evks['aud/left'].plot_field(maps, time=0.1)


for ch_type in ('mag', 'grad', 'eeg'):
    evk = evks['aud/right'].copy().pick(ch_type)
    _map = mne.make_field_map(evk, trans=sample_data_trans_file,
                              subject='sample', subjects_dir=subjects_dir,
                              meg_surf='head')
    fig = evk.plot_field(_map, time=0.1)
    mne.viz.set_3d_title(fig, ch_type, size=20)
